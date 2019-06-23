Source: https://gist.github.com/ex-nerd/22d0a9796f4f5df7080f9ac5a07a381f

```
Martins-MacBook-Pro:clean-up-slicer martin$ python cleanup_prusa_slic3r_gcode.py --help
usage: cleanup_prusa_slic3r_gcode.py [-h] [--verbose] [--keepcomments]
                                     [--defaulttool [DEFAULTTOOL]]
                                     [--targetfolder [TARGETFOLDER]]
                                     [--overwrite]
                                     filenames [filenames ...]

Gcode cleaner to work around some multi-extruder bugs in slic3r Prusa edition.

positional arguments:
  filenames             One or more paths to .gcode files to clean

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Enable additional debug output
  --keepcomments        keep comments
  --defaulttool [DEFAULTTOOL]
                        default tool like "T0"
  --targetfolder [TARGETFOLDER]
                        target folder like "z:\\printing"
  --overwrite           Overwrite the input file
```
#Example:
```
Martins-MacBook-Pro:clean-up-slicer martin$ python cleanup_prusa_slic3r_gcode.py --keepcomments --verbose Echo.gcode


Starting conversion:


Default Tool: T0
Target-Folder: /Users/martin/dev/git-repos/3d/clean-up-slicer
Keep comments: False
overwrite source file: False
source files:
 * Echo.gcode


Echo.gcode => /Users/martin/dev/git-repos/3d/clean-up-slicer/Echo.prusaclean.gcode
```
