# CSCI 1101 Computer Science 1
#
# This program displays an NxN grid of randomly colored squares.
# Clicking stops or starts.
#
# run: python3 tickSquares.py N

from animate import *
from enum import Enum
import random, time, sys

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
    def __init__(self, n, row, col, image, state):
        self.n = n
        self.row = row
        self.col = col
        self.image = image
        self.state = state

# view : model -> image
def view(model):
    return model.image
        
# touchUpdate : model * (int * int) * event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up:
        newState = toggle(model.state)
        return Model(model.n, model.row, model.col, model.image, newState)
    else:
        return model

# tickUpdate : model -> model
def tickUpdate(model):
    if model.state == State.Idle:
        return model
    else:
        if model.row == 0 and model.col == 0:
            model.image = backing
        side = WIDTH // model.n
        square = Image.rectangle(side, side, Color.random())
        (x, y) = (model.col * side, model.row * side)
        image = Image.placeImage(square, (x, y), model.image)
        time.sleep(1)
        if model.col < model.n - 1:
            return Model(model.n, model.row, model.col + 1, image, model.state)
        else:
            return Model(model.n, model.row + 1, 0, image, model.state)

# finished : model -> boolean        
def finished(model):
    return model.row == model.n

def go():
    n = 0
    if len(sys.argv) == 2:
        n = int(sys.argv[1])
    else:
        print("run: python3 tickSquares.py N")
        sys.exit()
    
    initialModel = Model(n, 0, 0, splash, State.Idle)

    Animate.start(model=initialModel,
                  view=view,
                  touchUpdate=touchUpdate,
                  tickUpdate=tickUpdate,   # model -> model
                  stopWhen=finished,       # model -> boolean
                  viewLast=view)           # model -> image

go()
