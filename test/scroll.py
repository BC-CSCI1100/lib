# CSCI 1100 Gateway to Computer Science
#
# This program scrolls a string left to right. Arrow keys
# alter the location of the string.
#
# run: python3 scroll.py

import os

from animate import *
from enum import Enum

os.environ['DISPLAY'] = ': 0.0'

backing = Image.rectangle(WIDTH, HEIGHT, Color.Red)
text = Image.text("CSCI 1100", Color.White, size=50)

# An enumeration of states.
class State(Enum):
    Stop = 0
    Start = 1

# toggle : state -> state
def toggle(state):
    if state == State.Stop:
        return State.Start
    else:
        return State.Stop

# Using a class here to define a record -- only creation and field projection.
class Model():
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

# view : model -> image
def view(model): 
    return Image.placeImage(text, (model.x, model.y), backing)

# tickUpdate : model -> model
def tickUpdate(model):
    if model.state == State.Start:
        if model.x > WIDTH:
            model.x = -200
        return Model(model.x + 3, model.y, model.state)
    else:
        return model
    
# touchUpdate : model * (x, y) * event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up:
        return Model(model.x, model.y, toggle(model.state))
    else:
        return model

# keyUpdate : model * keyname -> model    
def keyUpdate(model, key):
    if key == "left":
        return Model(model.x - 10, model.y, model.state)
    if key == "right":
        return Model(model.x + 10, model.y, model.state)
    if key == "up":
        return Model(model.x, model.y - 10, model.state)
    if key == "down":
        return Model(model.x, model.y + 10, model.state)
    else:
        return model

# finished : model -> boolean    
def finished(model):
    return False

initialModel = Model(0, 375, State.Start)

Animate.start(model=initialModel,
              view=view,               # model -> image
              tickUpdate=tickUpdate,   # model -> model
              touchUpdate=touchUpdate, # model * (x, y) * event -> model
              keyUpdate=keyUpdate,     # model * keyname -> model
              stopWhen=finished)       # model -> boolean
