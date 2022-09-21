# CSCI 1100 Gateway to Computer Science
#
# This program displays an animation of Conway's game of life.
# Clicking stops or starts.
#
# run: python3 life.py inputfile.txt

import importlib
from animate import *
from enum import Enum
import sys

PACE = 0.05

# Backgrounds

AliveColor = Color.Orange
NotAliveColor = Color.White
BackgroundColor = Color.White

# Make splash panels with instructions.
_ins1 = Image.text("Click to start/stop", Color.White, size=50)
_ins2 = Image.text("^/v to speed up/slow down", Color.White, size=50)
backSplash = Image.rectangle(WIDTH, HEIGHT, Color.DarkGray)
splash1    = Image.placeImage(_ins1, (WIDTH // 2 - 225, HEIGHT // 2 - 30), backSplash)
splash2    = Image.placeImage(_ins2, (WIDTH // 2 - 350, HEIGHT // 2 - 30), backSplash)

# Inhabited cells are either alive or not alive
class Status(Enum):
    Uninhabited = 0
    Alive = 1
    NotAlive = 2

def colorOf(status):
    if status == Status.Alive:       return AliveColor
    if status == Status.NotAlive:    return NotAliveColor
    if status == Status.Uninhabited: return Color.Black

class State(Enum):
    Ready   = 0
    Launch  = 1
    Running = 2
    Paused  = 3

# transition : state -> state
def transition(state):
    if state == State.Ready:   return State.Launch
    if state == State.Launch:  return State.Running
    if state == State.Running: return State.Paused
    if state == State.Paused:  return State.Running

# Using a class as a record -- only creation and field projection.
class Model():
    def __init__(self, state, image, colony, workarea, pace):
        self.state    = state
        self.image    = image
        self.colony   = colony
        self.workarea = workarea
        self.pace     = pace

# dimensions : 2D array -> (int * int)
def dimensions(a):
    return (len(a), len(a[0]))

# view : model -> image
def view(model):
    (colony, workarea) = (model.colony, model.workarea)
    (rows, cols) = (len(colony) - 2, len(colony[0]) - 2)
    width = (HEIGHT * cols) // rows
    cellWidth, cellHeight = width // cols, HEIGHT // rows
    for row in range(1, len(colony) - 1):
        for col in range(1, len(colony[row]) - 1):
            colonist = colony[row][col]
            if isAlive(colonist) or colonist != workarea[row][col]:
                (x, y) = (row - 1) * cellHeight, (col - 1) * cellWidth
                img = Image.circle(cellWidth // 2, colorOf(colonist))
                model.image = Image.placeImage(img, (x, y), model.image)

    if model.state == State.Ready:
        return splash1
    if model.state == State.Launch:
        return splash2
    else:
        return model.image
    
# touchUpdate : model * (int * int) * event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up:
        state = transition(model.state)
        return Model(state,
                     model.image,
                     model.colony,
                     model.workarea,
                     model.pace)
    else:
        return model

# count : 2Darray * int * int -> int       count living neighbors
def count(a, row, col):
    n = 0
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if a[i][j] == Status.Alive:
                n = n + 1
    return (n - 1) if a[row][col] == Status.Alive else n  # don't count self

# isAlive : status -> boolean
def isAlive(status): return status == Status.Alive

# keyUpdate : model * keyname -> model
def keyUpdate(model, key):
    if key == "up":                              # speed up
        model.pace = max(0.0, model.pace - 0.1)
    if key == "down":                            # slow down
        model.pace = model.pace + 0.1
    return model

# tickUpdate : model -> model
def tickUpdate(model):
    if model.state != State.Running:
        return model
    for row in range(1, len(model.colony) - 1):
        for col in range(1, len(model.colony[row]) - 1):
            n = count(model.colony, row, col)
            
            if isAlive(model.colony[row][col]):
                status = Status.Alive if n == 2 or n == 3 else Status.NotAlive
            else:
                # model.colony[row][col] isn't alive
                status = Status.Alive if n == 3 else Status.NotAlive
                
            model.workarea[row][col] = status

    time.sleep(model.pace)
    # NB: switching colony and workarea in the new model
    return Model(model.state,
                 model.image,
                 model.workarea,
                 model.colony,
                 model.pace)

def makeArray(rows, cols, item):
    return [[ item for _ in range(cols)] for _ in range(rows)]

# confirmSquare : string list -> string list
def confirmSquare(lines):
    nLines = len(lines)
    for i in range(nLines):
        nChars = len(lines[i])
        if nChars != nLines:
            print(f'Input file should be square. There are {nLines} lines.')
            print(f'But line {i} has {nChars} characters. Repairing.')
            if nChars < nLines:   # add padding
                padding = ''.join([ '.' for _ in range(nLines - nChars)])
                lines[i] = lines[i] + padding
            else:
                # nChars > nLines, truncate
                lines[i] = lines[i][0:nLines]
    return lines
                              
# initialColony : filename -> (2D-array of status * 2D-array of status)
def initialColony(file):
    with open(file) as inch:
        lines = inch.read().splitlines()
    lines = confirmSquare(lines)           # Fix any jagged edges

    # + 2 adds a border to simplify neighbor counting
    rows, cols = len(lines) + 2, len(lines[0]) + 2
    colony     = makeArray(rows, cols, Status.Uninhabited)
    workarea   = makeArray(rows, cols, Status.Uninhabited)

    for row in range(rows - 2):
        line = lines[row]
        for col in range(cols - 2):
            ch = line[col]
            colony[col+1][row+1] = Status.Alive if ch == '*' else Status.NotAlive
    return (colony, workarea)

def go(cmdLineInputs):
    if len(cmdLineInputs) != 2:
        print("run: python3 life.py inputfile")
        sys.exit()
    else:
        inputFile = cmdLineInputs[1]
        (colony, workarea) = initialColony(inputFile)
        (rows, cols) = (len(colony) - 2, len(colony[0]) - 2)
        # With height as HEIGHT and height/rows == width/cols
        width  = (HEIGHT * cols) // rows        
        image = Image.rectangle(width, HEIGHT, BackgroundColor)
        initialModel = Model(State.Ready, image, colony, workarea, PACE)
        Animate.start(model       = initialModel,
                      view        = view,
                      keyUpdate   = keyUpdate,
                      tickUpdate  = tickUpdate,
                      touchUpdate = touchUpdate,
                      stopWhen    = lambda _ : False)

go(sys.argv)
