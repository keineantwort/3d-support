```
Martins-MacBook-Pro:add-led-progress martin$ ./add-led-progress.py --help
usage: add-led-progress.py [-h] [--verbose] [--overwrite]
                           filenames [filenames ...]

Gcode manipulation. Adds LED commands for progress.

positional arguments:
  filenames      One or more paths to .gcode files to extend with progress
                 information

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v  Enable debug output
  --overwrite    Overwrite the input file (default is FALSE)
```
#Example:
```
Martins-MacBook-Pro:add-led-progress martin$ ./add-led-progress.py Echo.gcode
Total number of lines: 112742
Number of lines (w/o comments): 112742
Number of lines per percent: 1127.000000
Echo.gcode => Echo.ledextended.gcode
```
