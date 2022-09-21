# CSCI 1100 Gateway to Computer Science
#
# This program scrolls a string left to right. Arrow keys
# alter the location of the string.
#
# run: python3 scroll2.py

from animate import *
from enum import Enum

# toggle : state -> state
def toggle(state):
    return not(state)

# Use a Python class to define a simple record structure with two named fields.
class Model():
    def __init__(self, paused=False, x=0):
        self.paused = paused
        self.x = x

# view : model -> image
def view(model):
    backing = Image.rectangle(WIDTH, HEIGHT, Color.Red)
    text    = Image.text("Gateway", Color.White, size=100)
    return Image.placeImage(text, (model.x, 325), backing)

# tickUpdate : model -> model
def tickUpdate(model):
    if model.paused:
        return model
    else:
        x = model.x + 3 if model.x < WIDTH else -400
        return Model(paused=model.paused, x=x)

# touchUpdate : model * (x, y) * event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up:
        return Model(paused=toggle(model.paused), x=model.x)
    else:
        return model

# finished : model -> boolean
def finished(model):
    return False

initialModel = Model(paused=False, x=0)

Animate.start(model=initialModel,
              view=view,               # model -> image
              tickUpdate=tickUpdate,   # model -> model
              touchUpdate=touchUpdate, # model * (x, y) * event -> model
              stopWhen=finished)       # model -> boolean
