# CSCI 1100 Gateway to Computer Science
#
# This program displays a PNG image.
#
# run: python3 pngShow.py pngfile

from animate import *

def go():
    if len(sys.argv) == 2:
        Animate.show(sys.argv[1])
    else:
        print("run: python3 pngShow.py pngfile")
        sys.exit()

go()
