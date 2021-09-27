hex2dfcolors
============

A Python 3 tool for converting color list files
to Dwarf Fortress `colors.txt` color scheme files.

Usage
-----

```shell
hex2dfcolors.py COLOR_FILE OUTPUT
```

`COLOR_FILE`
: Path to the color list file

`OUTPUT`
: colors.txt file path

Color list file format
----------------------

### Example

```
black=#282828
red=#cc241d
green=#98971a
brown=#d79921
blue=#458588
magenta=#b16286
cyan=#689d6a
lgray=#a89984
dgray=#928374
lred=#fb4934
lgreen=#b8bb26
lyellow=#fabd2f
lblue=#83a598
lmagenta=#d3869b
lcyan=#83c07c
white=#ebdbb2
```

Usage of RGB colors
in `rgb(R, G, B)` format
is also acceptable, as well as
no `#` in the HEX format.
