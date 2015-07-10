#rosti

_**rosti** - A swiss dish consisting mainly of potatoes._

## Usage

```
$ rosti /some/directory
Checked a total of 23985 files in 17677 directories, of which 28 are suspect.

/some/directory/a_file.php
    0: Code from 0-510 is long (510 vs 475).

Cleaning:
Cleaning not requested (use --clean).

Finished.
```

## What?

After a large scale infection of a number of sites I found that removing all the code that had been added to PHP files
was proving to be very time consuming. The scope of the infection was also difficult to assess and while in an ideal
world I would have simply replaced all the possibly infected code, a number of my clients would have found this impossible
to accomplish without a lot of assistance. Given all of this, I wrote this small script and started looking at the malicious
code in order to be able to detect patterns.

I recognise that this approach is flawed for any long term solution, but at present it works and has saved me many hours!

I'm making this available as it was useful for me and might save someone some time in the future!

## Usage Examples

To scan a directory and report on possibly infected files.

> $ rosti /some/directory

To scan, clean and report.

> $ rosti /some/directory --clean

## Future

This script will be joining my toolkit, so I'll try and keep it updated and working :-)

One good suggestion is to add the ability for a comparison to be made of files and file sizes with a "clean" copy of wordpress to highlight additional files or files that have been altered. I may try and add this.

There are a few things that would be useful to do.

- better reporting of what has been done
- improve the removal logic

## Help Welcome!

If you have ideas, suggestions or patches let me know!
