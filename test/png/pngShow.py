from animate import *

# CSCI 1101 Computer Science 1
#
# This program displays a PNG image.
#
# run: python3 pngShow.py pngfile

def go():
    if len(sys.argv) == 2:
        Animate.show(sys.argv[1])
    else:
        print("run: python3 pngShow.py pngfile")
        sys.exit()

go()
