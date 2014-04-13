#!/usr/bin/env python
"""Usage:
  print_label.py -p <printer> [options] <text>

  Options:
    -h --help                         Show this help message
    -p <printer>, --printer=<printer>  Printer name as known to CUPS
    -f <font>, --font=<font>           Name of the font to use (must be a .ttf font in
                                       the 'fonts' directory) [default: Lato-Bold]
    -s <size>, --size=<size>           Font size [default: 60]

"""

from docopt import docopt
from labelprinter import LabelPrinter

if __name__ == "__main__":

    arguments = docopt(__doc__)

    labelprinter = LabelPrinter(arguments['--printer'])
    labelprinter.printLabel(arguments['<text>'], arguments['--font'], int(float(arguments['--size'])))
