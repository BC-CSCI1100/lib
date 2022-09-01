# CSCI 1101 Computer Science 1
#
# This program displays an NxN grid of randomly colored squares.
# Click to place a square.
#
# run: python3 touchSquares.py N

from animate import *
from enum import Enum
import random, time, sys

# CSCI 1101 Computer Science 1
#
# This program displays an NxN grid of randomly colored squares.
# Clicking stops or starts.
#
# run: python3 tickSquares.py N

# Backgrounds
backing = Image.rectangle(WIDTH, HEIGHT, Color.DarkGray)
instruction = Image.text("Click", Color.White, 80)
_x, _y = HEIGHT // 2 - 100, WIDTH // 2 - 40
splash = Image.placeImage(instruction, (_x, _y), backing)

# The program is either idle or running. Clicking toggles the state.
#
class State(Enum):
    Idle = 0
    Running = 1

# toggle : state -> state
def toggle(state):
    if state == State.Idle:
        return State.Running
    else:
        return State.Idle

# Using a class here as a record -- only creation and field projection.
#
class Model():
    def __init__(self, n, image, state):
        self.n = n
        self.image = image
        self.state = state

# view : model -> image
def view(model):
    return model.image
        
# touchUpdate : model * (int * int) * event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up and model.state == State.Idle:
        newState = toggle(model.state)
        return Model(model.n, backing, newState)
    if event == Touch.Up:
        side = WIDTH // model.n
        square = Image.rectangle(side, side, Color.random())
        (x0, y0) = xy
        (col, row) = (x0 // side, y0 // side)                # NB integer division
        (x, y) = (col * side, row * side)
        image = Image.placeImage(square, (x, y), model.image)
        return Model(model.n, image, model.state)
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
        print("run: python3 touchSquares.py N")
        sys.exit()
    
    initialModel = Model(n, splash, State.Idle)

    Animate.start(model=initialModel,
                  view=view,
                  touchUpdate=touchUpdate,
                  stopWhen=finished)       # model -> boolean

go()
