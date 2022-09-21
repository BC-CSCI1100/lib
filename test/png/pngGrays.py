# CSCI 1100 Gateway to Computer Science
#
# This program displays a color image, then black and white, then halftone.
#
# run: python3 pngGrays.py filename.png

from animate import *
import sys

# Instruction for the splash page
instruction = Image.text("Click", Color.White, 80)

class State(Enum):
    Start = 0
    Color = 1
    BlackAndWhite = 2
    HalfTone = 3

# Using class as a record here -- only construction and field projection.
# NB: the splash page is in the model because we're going to open a png
# file and we need the splash page to be the size of the png.
class Model():
    def __init__(self, state, splash, image, width, height):
        self.state = state
        self.splash = splash
        self.image = image
        self.width = width
        self.height = height

# view : model -> image
def view(model):
    return model.splash if model.state == State.Start else model.image

# blackAndWhite : image * int * int -> image
def blackAndWhite(image, width, height):
    pixels = Image.toArray(image)
    for row in range(height):
        for col in range(width):
            color = pixels[row][col]
            red   = Color.red(color)
            green = Color.green(color)
            blue  = Color.blue(color)
            gray  = (red + green + blue) // 3
            pixels[row][col] = Color.make(gray, gray, gray) 
    return Image.fromArray(pixels)

# halfTone : image * int * int -> image
def halfTone(image, width, height):
    pixels = Image.toArray(image)
    for row in range(height):
        for col in range(width):
            red = Color.red(pixels[row][col])
            ht = Color.Black if red < 128 else Color.White
            pixels[row][col] = ht
    return Image.fromArray(pixels)

# touchUpdate : model -> (int * int) -> event -> model
def touchUpdate(model, xy, event):
    if event == Touch.Up:
        if model.state == State.Start:
            return Model(State.Color, None, model.image, model.width, model.height)
        if model.state == State.Color:
            bw = blackAndWhite(model.image, model.width, model.height)
            return Model(State.BlackAndWhite, None, bw, model.width, model.height)
        if model.state == State.BlackAndWhite:
            ht = halfTone(model.image, model.width, model.height)
            return Model(State.HalfTone, None, ht, model.width, model.height)
        else:
            sys.exit(1)
    else:
        return model
    
def go():
    filename = ""
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        print("run: python3 pngGrays.py filename.png")
        sys.exit()

    image = Image.read(filename)
    (width, height) = Image.dimensions(image)
    _x, _y = width // 2 - 100, height // 2 - 40
    backing = Image.rectangle(width, height, Color.DarkGray)
    splash = Image.placeImage(instruction, (_x, _y), backing)
    initialModel = Model(State.Start, splash, image, width, height)
    Animate.start(model  = initialModel,
                  width  = width,
                  height = height,
                  view   = view,
                  touchUpdate = touchUpdate,
                  stopWhen = lambda _ : False)

go()
