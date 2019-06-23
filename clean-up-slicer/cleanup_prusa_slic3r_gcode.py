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


def comment(str):
    return '; ' + str

def write(str, outfile, delete_comments=False):
    if delete_comments:
        if not str.startswith(';'):
            outfile.write(re.sub(';.*', '', str))
    else:
        outfile.write(str)

def rewrite(infile, outfile, verbose=False, delete_comments=False, my_tool_default='T0'):
    WIPE = 1
    UNLOAD = 2
    LOAD = 3
    toolchange = 0
    priming = False
    temp_change = None
    my_tool = my_tool_default+'\r\n'
    for line in infile:
        if line.startswith('\r\n'):
            continue

        # Priming
        if line.startswith('; CP PRIMING'):
            if 'START' in line:
                priming = True
            elif 'STOP' in line:
                priming = False
        # Detect toolchange state
        elif line.startswith('; CP TOOLCHANGE'):
            if 'WIPE' in line:
                toolchange = WIPE
            elif 'UNLOAD' in line:
                toolchange = UNLOAD
            elif 'LOAD' in line:
                toolchange = LOAD
            else:
                toolchange = 0

        # Process the various lines
        if line.startswith(';'):
            write(line, outfile, delete_comments)
        elif line.rstrip() in ('G4 S0', ):
            write(comment(line), outfile, delete_comments)
        elif line.startswith('M907 '):
            write(comment(line), outfile, delete_comments)
        elif priming:
            write(comment(line), outfile, delete_comments)
        elif toolchange in (LOAD, UNLOAD):
            if line.startswith('G1'):
                # Only remove integer-value E moves (part of the Prusa load/unload routine?)
                # The other E values appear to be part of the actual wipe tower.
                if re.search(r'E-?\d+\.0000', line):
                    write(comment(line), outfile, delete_comments)
                else:
                    write(line, outfile, delete_comments)
            elif line.startswith('T'):
                my_tool = line
                write(line, outfile, delete_comments)
                if temp_change:
                    # Duplicate the last temperature change.
                    # https://github.com/prusa3d/Slic3r/issues/559
                    write(temp_change, outfile, delete_comments)
                    temp_change = None
            else:
                if line.startswith('M104 S'):
                    temp_change = line
                write(line, outfile, delete_comments)
        # retract on T3
        elif line.startswith('G10'):
            write('T3\n'+line, outfile, delete_comments)
        # unretract on T3
        elif line.startswith('G11'):
            write(line+my_tool, outfile, delete_comments)
        else:
            write(line, outfile, delete_comments)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Gcode cleaner to work around some multi-extruder bugs in slic3r Prusa edition.'
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
        '--keepcomments',
        action='store_false',
        help="keep comments",
    )
    parser.add_argument(
        '--defaulttool',
        help="default tool like \"T0\" ",
        nargs='?',
        default='T0',
    )
    parser.add_argument(
        '--targetfolder',
        help="target folder like \"z:\\\\printing\" ",
        nargs='?',
        default=os.getcwd(),
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
        help="One or more paths to .gcode files to clean",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.verbose:
        print('\r\n\r\nStarting conversion: \r\n\r\n')
        print('- Default Tool: {}'.format(args.defaulttool))
        print('- Target-Folder: {}'.format(args.targetfolder))
        print('- Keep comments: {}'.format(args.keepcomments))
        print('- overwrite source file: {}'.format(args.overwrite))
        print('- source files:')
        for infile in args.filenames:
            print('   * {}'.format(infile.name))
        print('\r\n')

    for infile in args.filenames:
        infilename = infile.name
        tmpfilename = os.path.join(args.targetfolder, '{}.tmp{}'.format(*os.path.splitext(infilename)))
        with open(tmpfilename, 'w') as tmpfile:
            rewrite(infile, tmpfile, args.verbose, args.keepcomments, args.defaulttool)
        infile.close()
        if args.overwrite:
            os.rename(infilename, "{}.bak".format(infilename))
            outfilename = infilename
        else:
            outfilename = os.path.join(args.targetfolder, '{}.prusaclean{}'.format(*os.path.splitext(infilename)))
        os.rename(tmpfilename, outfilename)
        print("{} => {}".format(infilename, outfilename))
        