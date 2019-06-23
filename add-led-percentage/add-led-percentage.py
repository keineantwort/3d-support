#!/usr/bin/env python
"""
Gcode cleaner to work around prusa slic3r annoyances for multi-filament
single-tool printing on non-Prusa printers.

This gist can be found here:
* https://gist.github.com/ex-nerd/22d0a9796f4f5df7080f9ac5a07a381f

Bugs this attempts to work around:
* https://github.com/prusa3d/Slic3r/issues/557
* https://github.com/prusa3d/Slic3r/issues/559
* https://github.com/prusa3d/Slic3r/issues/560
"""

import os
import re
import argparse

def addled(infile, outfile, verbose=False, skip_comments=False):
    lines = [line for line in infile]
    num_lines = sum(1 for line in lines) # 100%
    
    #lines per percent
    lines_per_percent = num_lines / 100

    if verbose:
        print('Number of lines: {:d}'.format(num_lines))
        print('Number of lines per percent: {:f}'.format(lines_per_percent))

    line_count = 0
    percent = 0
    for line in lines:
        line_count = line_count + 1
        if line_count > lines_per_percent:
            line_count = 0
            percent = percent + 1
            outfile.write('; Percent = {:d}\n'.format(percent))
            print('; Percent = {:d}'.format(percent))
        outfile.write(line)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Gcode manipulation. Adds LED commands for progress.'
    )
    parser.set_defaults(
        verbose=False,
        overwrite=False,
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Enable additional debug output",
    )
    parser.add_argument(
        '--skipcomments',
        action='store_false',
        help="skip comments while counting lines",
    )
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help="Overwrite the input file",
    )
    parser.add_argument(
        'filenames',
        type=argparse.FileType('r'),
        nargs='+',
        help="One or more paths to .gcode files to extend",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.verbose:
        print('\r\n\r\nStarting conversion: \r\n\r\n')
        print('- skip comments: {}'.format(args.skipcomments))
        print('- overwrite source file: {}'.format(args.overwrite))
        print('- source files:')
        for infile in args.filenames:
            print('   * {}'.format(infile.name))
        print('\r\n')
    for infile in args.filenames:
        infilename = infile.name
        tmpfilename = '{}.tmp{}'.format(*os.path.splitext(infilename))
        with open(tmpfilename, 'w') as tmpfile:
            addled(infile, tmpfile, args.verbose, args.skipcomments)
        infile.close()
        if args.overwrite:
            os.rename(infilename, "{}.bak".format(infilename))
            outfilename = infilename
        else:
            outfilename = '{}.ledextended{}'.format(*os.path.splitext(infilename))
        os.rename(tmpfilename, outfilename)
        print("{} => {}".format(infilename, outfilename))