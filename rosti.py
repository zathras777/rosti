from email.mime.text import MIMEText

import os
import sys
import argparse
import re
import smtplib
import subprocess

EMAIL_FROM = None

class PhpFile(object):
    SUSPECT_RE = re.compile("^\<\?(php)?")
    TAG_RE = "\<\?(php)?(.*?)\?\>"
    CHECKS = [
        (re.compile("^<\?(php)? \$[a-z]{6,} \= \"[a-f0-9]{5,}\"; preg_replace\(\".*?\",\".*?\",\".*?\"\); \?>"),
         "preg_replace code detected"),
        (re.compile("^<\?(php)? \$([a-z]{5,}) = .*function_exists"),
         "function...for code detected"),
        (re.compile(".*\!isset\(\$GLOBALS\[\""),
         "!isset($GLOBALS[ detected"),
        (re.compile(".*eval\((gzinflate|base64_decode)\("),
         "eval code with inflate/base64_decode detected"),
        (re.compile("^<\?(php)?\s+(\$\w+)=\".*\\2\[\d+\]\.\\2\[.*eval"),
         "substring replacement code detected")
    ]
    LENGTH_WARN = 475

    def __init__(self, fn):
        self.filename = fn
        self.keep_original = False
        self.suspect_lines = []
        with open(fn, 'r') as fh:
            ln = 0
            for line in fh.readlines():
                if self.SUSPECT_RE.match(line) and \
                                len(line) > self.LENGTH_WARN:
                    self.suspect_lines.append((ln, line))
                ln += 1

    def possibly_infected(self):
        return len(self.suspect_lines) > 0

    def check(self):
        info = []
        for (ln, suspect) in self.suspect_lines:
            for m in re.finditer(self.TAG_RE, suspect):
                ck = self._check_match(m)
                if ck is not None:
                    info.append("{}: {}".format(ln, ck))
        return info

    def clean(self):
        new_lines = []
        old_lines = []
        cleaned = 0
        with open(self.filename, 'r') as fh:
            for line in fh.readlines():
                line = line.strip()
                old_lines.append(line)
                if re.search(self.TAG_RE, line) is None:
                    new_lines.append(line)
                else:
                    kept = ''
                    last = 0
                    for m in re.finditer(self.TAG_RE, line):
                        if m.start() != last:
                            kept += line[last:m.start()]
                        ck = self._check_match(m, True)
                        if ck is None:
                            kept += m.group(0)
                        else:
                            cleaned += 1
                        last = m.end()
                    if last != len(line):
                        kept += line[last:]
                    new_lines.append(kept)

        if self.keep_original:
            fn, ext = os.path.splitext(self.filename)
            with open(fn+'_original'+ext, 'w') as out:
                out.write("\n".join(old_lines))

        if len("".join(new_lines)) == 0:
            os.unlink(self.filename)
            return "DELETED: {} as cleaning resulted in empty file".format(self.filename)

        with open(self.filename, 'w') as fh:
            fh.write("\n".join(new_lines))

        if cleaned == 0:
            return "SKIPPED: {} due no pattern matches".format(self.filename)
        return "CLEANED: {} ({} patterns)".format(self.filename, cleaned)

    def _check_match(self, match, cleaning=False):
        for chk in self.CHECKS:
            if chk[0].match(match.group(0)) is not None:
                return chk[1]

        if cleaning:
            return None

        if match.end() - match.start() > self.LENGTH_WARN:
            return "Code from {}-{} is long ({} vs {}).".format(
                match.start(), match.end(), len(match.group(0)),
                self.LENGTH_WARN)
        return None

def print_report(php):
    print("\n{}".format(php.filename))
    for info in php.check():
        print("    {}".format(info))


def main():
    parser = argparse.ArgumentParser(description='rosti: a PHP infected file scanner')

    parser.add_argument('--clean', action='store_true', help='Clean infected files.')
    parser.add_argument('--no-report', action='store_false', help='No report')
    parser.add_argument('--keep-original', action='store_true', help='Preserve original')
    parser.add_argument('directory', help="Directory to start scan from")

    args = parser.parse_args()

    suspect = []
    checked = dircount = 0
    for a, b, c in os.walk(args.directory):
        dircount += 1
        for fn in c:
            if fn.endswith('php'):
                php = PhpFile(os.path.join(a, fn))
                checked += 1
                if php.possibly_infected():
                    suspect.append(php)

    print("Checked a total of {} files in {} directories, of which {} are suspect.".format(
        checked, dircount, len(suspect)))

    ss = []
    for s in suspect:
        if s.check() != []:
            ss.append(s)

    suspect = ss
    if args.no_report:
        for s in suspect:
            print_report(s)

    print("\nCleaning:")
    if args.clean:
        info = []
        for s in suspect:
            if args.keep_original:
                s.keep_original = True
            info.append(s.clean())
        print("\nCleaning was performed:")
        for i in info:
            print("  {}".format(i))
    else:
        print("Cleaning not requested (use --clean).")

    print("\nFinished.")
    sys.exit(0)


if __name__ == '__main__':
    main()
