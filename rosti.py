from email.mime.text import MIMEText

import os
import sys
import argparse
import re
import smtplib
import subprocess

EMAIL_FROM = None

class ScanWordpress(object):
    ISSET_PATTERN = "<\?[php]?.*isset\(\$GLOBALS\["

    def __init__(self, where, email=None, keep_original=False):
        self.where = where
        self.email = email
        self.keep = keep_original
        self.php_files = []
        self.cleaned = False

        for a, b, c in os.walk(self.where):
            for fn in c:
                if fn.endswith('.php'):
                    self.php_files.append(os.path.join(a, fn))

        def scan_file(fn):
            with open(fn, 'r') as fh:
                for ln in fh.readlines():
                    if len(ln) > 256:
                        if re.search(self.ISSET_PATTERN, ln) is not None or 'rot13' in ln:
                            return True
            return False

        self.infected = [[f] for f in self.php_files if scan_file(f)]

    def clean_files(self, prefix=None):
        details = []
        for info in self.infected:
            details.extend(self._clean_file(info[0], prefix))
        self.cleaned = True
        return details

    def _clean_file(self, fn, prefix=None):
        info = []
        new_lines = []
        original = []
        n = 0

        with open(fn, 'r') as fh:
            lines = original = [l.strip() for l in fh.readlines()]
            while n < len(lines):

                ln = lines[n]
                found = False

                # isset
                ck = re.search(self.ISSET_PATTERN, ln)
                if ck is not None:
                    info.append("isset: removed from line {}".format(n))

                    for tags, rqd, add in [(ln.split('><'), 1, '<'),
                                           (ln.split("<?php"), 2, '<?php'),
                                           (ln.split(' ?>'), 1, '')]:
                        if len(tags) > rqd:
                            new_lines.append(add + tags[-1])
                            break
                    found = True

                # @assert(str_rot13
                if '@assert(str_rot13' in ln:
                    info.append('rot13: removed line {}'.format(n))
                    if '//##' in lines[n + 1]:
                        n += 1
                    if lines[n + 1] == '?>' and new_lines[-2] == '<?php':
                        n += 1
                        del new_lines[-2]
                    if '//##' in new_lines[-1]:
                        new_lines.pop()
                    found = True

                if not found:
                    new_lines.append(ln)

                n += 1

        new_fn = fn
        if prefix is not None:
            name, ext = os.path.splitext(fn)
            new_fn = "{}_{}{}".format(name, prefix, ext)

        with open(new_fn, 'w') as fh:
            fh.write("\n".join(new_lines))

        if self.keep:
            with open(fn + '.hacked', 'w') as fh:
                fh.write("\n".join(original))

        return info

    def report(self):
        rv = "Possibly infected file report for '{}'.\n\n".format(self.where)
        rv += "Total of {} files require attention:\n".format(len(self.infected))
        for info in sorted(self.infected):
            rv += "    {}\n".format(info[0])
            rv += "\n".join(["        - {}".format(xtra) for xtra in info[1:]])
            if len(info) > 1:
                rv += '\n'
        if self.keep and self.cleaned:
            rv += "\nDiffs..."
            for info in sorted(self.infected):
                p = subprocess.Popen(['diff', '-u', info[0]+'.hacked', info[0]],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                out, err = p.communicate()
                rv += out + "\n\n"
        return rv

    def send_report(self):
        if self.email is None or EMAIL_FROM is None:
            return False

        msg = MIMEText(self.report())
        msg['Subject'] = 'Infected File Report for '.format(self.where)
        msg['From'] = EMAIL_FROM
        msg['To'] = self.email

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(EMAIL_FROM, [self.email], msg.as_string())
        s.quit()

        return True

    def cleanup(self):
        if not self.cleaned or not self.keep:
            return
        for info in sorted(self.infected):
            os.unlink(info[0]+'.hacked')

    def is_infected(self):
        return len(self.infected) > 0


def main():
    parser = argparse.ArgumentParser(description='rosti Wordpress rot13 exploit remover')

    parser.add_argument('--report-only', action='store_true',
                        help='Just report on infected files.')
    parser.add_argument('--no-report', action='store_true', help='No report, just clean')
    parser.add_argument('--from', dest='from_email', help='Email address reports will be sent from')
    parser.add_argument('--email', help='Email address to send report')
    parser.add_argument('--email-file', help='File with email addresses to use for sites')
    parser.add_argument('--diffs', action='store_true', help='Keep original files and produce diffs')

    parser.add_argument('directory', help="Directory to start scan from")

    args = parser.parse_args()

    if args.report_only and args.no_report:
        print("You cannot use '--report-only' and '--no-report' flags at the same time!")
        sys.exit(0)

    if args.from_email is not None:
        EMAIL_FROM = args.from_email

    site_emails = {}
    if args.email_file is not None:
        with open(args.email_file, 'r') as fh:
            for ln in fh.readlines():
                if '#' in ln:
                   ln, ignored = ln.strip().split('#', 1)
                if len(ln) == 0:
                    continue
                print(len(ln), ln)
                path, email = re.split('[ |\t|\:]', ln)
                site_emails[path.strip()] = email.strip()

    sites = []
    reports = {}
    for a, b, c in os.walk(args.directory):
        if 'wp-content' in b and 'wp-admin' in b:
            sites.append(a)
        if 'configuration.php' in c and 'joomla.xml' in c:
            sites.append(a)


    print("Total of {} sites to scan...".format(len(sites)))

    for wp in sites:
        sc = ScanWordpress(wp, site_emails.get(wp), args.diffs)
        if len(sc.infected) == 0:
            print("  skipped {} as no infected files found...".format(sc.where))
            continue

        if not args.report_only:
            sc.clean_files()

        if not args.no_report:
            if not sc.send_report():
                reports[wp] = sc.report()
        sc.cleanup()

    print("Completed.")
    if args.no_report:
        sys.exit(0)

    if len(reports):
        if args.email is not None:
            if EMAIL_FROM is None:
                print("\nUnable to send mails as no source address specified. Use --from option.")
            else:
                msg = MIMEText("\n\n".join([reports[k] for k in reports]))
                msg['Subject'] = 'Infected File Reports'
                msg['From'] = EMAIL_FROM
                msg['To'] = args.email

                # Send the message via localhost SMTP server, but don't include the
                # envelope header.
                try:
                    s = smtplib.SMTP('localhost')
                    s.sendmail(EMAIL_FROM, [args.email], msg.as_string())
                    s.quit()
                    reports = []
                except:
                    print("Error sending mail, showing output instead.")

    if len(reports):
        print("\nNot sending reports as no default email address supplied...\n")
        for k in reports:
            print(reports[k])


if __name__ == '__main__':
    main()
