from animate import *
from enum import Enum
import random, time, sys

# CSCI 1101 Computer Science 1
#
# This program displays an NxN grid of randomly colored squares.
# Clicking stops or starts.
#
# run: python3 allSquares.py N

# The program is either idle or running. Clicking toggles the state.
#

# Backgrounds
backing = Image.rectangle(WIDTH, HEIGHT, Color.DarkGray)
instruction = Image.text("Click", Color.White, 80)
_x, _y = HEIGHT // 2 - 100, WIDTH // 2 - 40
splash = Image.placeImage(instruction, (_x, _y), backing)

# Using a class as a record here, only creation and field selection.
class Model():
    def __init__(self, n, image):
        self.n = n
        self.image = image

def makeGrid(n):
    side = WIDTH // n
    image = Image.rectangle(WIDTH, HEIGHT, Color.DarkGray)
    for row in range(n):
        for col in range(n):
            square = Image.rectangle(side, side, Color.random())
            (x, y) = (col * side, row * side)
            image = Image.placeImage(square, (x, y), image)
    return image
    
# view : model -> image
def view(model):
    return model.image
       
# touchUpdate : model * (int * int) * event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up:
        return Model(model.n, makeGrid(model.n))  # Install a grid in the model
    else:
        return model

# finished : model -> boolean        
def finished(model):
    return False

def go():
    n = 0
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    else:
        print("run: python3 allSquares.py N")
        sys.exit()
    initialModel = Model(n, splash)

    Animate.start(initialModel,
                  view=view,               # model -> image
                  touchUpdate=touchUpdate, # model * (int * int) * event -> model
                  stopWhen=finished)       # model -> boolean

go()
