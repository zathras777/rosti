#rosti

_**rosti** - A swiss dish consisting mainly of potatoes._

## Usage

```
$ rosti --report-only /some/directory
Total of 1 sites to scan...
Scanning /some/directory/subdir/wordpress
  skipped /some/directory/subdir/wordpress as no infected files found...
Completed.
```

## What?

After spending some hours trying to remove injected code from a Wordpress site following a compromise, I decided to write a script to automate the process. This is the result.

It scans for the code that I deal with, but should be easy enough to add additional patterns. It automates finding sites, which allows it to be used for a large number of sites without needing to worry about specifying every one. Additionally a file can be specified with paths to emails to allow reports to be sent to site owners, if desired.

It scans for both Wordpress and Joomla sites, though the detection of Joomla could be improved :-)

I'm making this available as it was useful for me and might save someone some time in the future!

## Usage Examples

To scan a directory and report on possibly infected files.

> $ rosti --report-only /some/directory

To scan and send a report via email.

> $ rosti --report-only --from source@domain.com --email person@domain.com /some/directory

To scan, clean and report.

> $ rosti --from source@domain.com --email person@domain.com /some/directory

To view everything that was done, you can get full diffs. However, this option generates a LOT of output and will probably exceed the email message size.

> $ rosti --diffs /some/directory

## Future

This script will be joining my toolkit, so I'll try and keep it updated and working :-)

One good suggestion is to add the ability for a comparison to be made of files and file sizes with a "clean" copy of wordpress to highlight additional files or files that have been altered. I may try and add this.

There are a few things that would be useful to do.

- compress the diffs and attach to an email
- better reporting of what has been done
- improve the removal logic

## Help Welcome!

If you have ideas, suggestions or patches let me know!
