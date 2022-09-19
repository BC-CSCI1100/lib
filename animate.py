import pygame, sys
from pygame.locals import *
from enum import Enum
import random, time
import numpy as np

WIDTH  = 800
HEIGHT = WIDTH
LINEWIDTH = 4
FONTSIZE = 50

# findMax : int list -> int, adding up the numbers, what is the smallest
# partial sum along the way?
#
def findMin(dxs):
    current = dxs[0]
    min = current
    for dx in dxs[1:]:
        current = current + dx
        if current < min:
            min = current
    return min

class Shape(Enum):
    Circle = 0
    Rectangle = 1
    Polygon = 2
    Line = 3
    Text = 4
    Image = 5
    Placed = 6

class Touch(Enum):
    Up = 0
    Down = 1

class Color:
    # Representing colors using pygame.Color

    def make(red, green, blue, alpha=255):
#        c = (((((alpha << 4) | blue) << 4) | green) << 4) | red
        return pygame.Color((red, green, blue, alpha))
   
    # Seems to be some issue here. i = 0xAARRGGBB where AA is alpha?
    # When reading from a png array, i seems to be 0xRRGGBBAA...
    def fromInteger(i):
        (a, b, g, r) = pygame.Color(i)    # These seem to be backwards!
        return Color.make(r, g, b, a)
     
    Red   =      make(0xFF,    0,    0)
    Green =      make(   0, 0xFF,    0)
    Blue  =      make(   0,    0, 0xFF)
    DodgerBlue = make(0x1E, 0x90, 0xFF)
    Black =      make(   0,    0,    0)
    White =      make(0xFF, 0xFF, 0xFF)
    Gray  =      make(0x7F, 0x7F, 0x7F)
    DarkGray  =  make(0x3F, 0x3F, 0x3F)
    LightGray =  make(0xBF, 0xBF, 0xBF)
    Orange =     make(0xFF, 0xA5, 0x00)

    # When working with bitmaps returned by Image.toArray, the color
    # is encoded as an int 0xAABBGGRR rather than a tuple. The branching
    # here is to alleviate the need for students to worry about converting.
    def red(color):
#        print("getting red")
        if isinstance(color, int):
#            print("color is an int, returning {:x}".format(color & 0x000000FF))
            return color & 0x000000FF
        else:
#            (a, b, g, r) = color
#            print("color is ({:x}, {:x}, {:x}, {:x}), returning {:x}".format(a, b, g, r, color.r))
            return color.r

    def green(color):
        if isinstance(color, int):
            return color & 0x0000FF00 >> 8
        else:
            return color.g

    def blue(color):
        if isinstance(color, int):
            return color & 0x00FF0000 >> 16
        else:
            return color.b

    def alpha(color):
        if isinstance(color, int):
            return color & 0xFF000000 >> 24
        else:
            return color.a

#    def red(color):   return color.r
#    def green(color): return color.g
#    def blue(color):  return color.b
#    def alpha(color): return color.a

    def random():
        return Color.make(random.randint(0, 0xFF),
                          random.randint(0, 0xFF),
                          random.randint(0, 0xFF))

class Image:
    # The representation type is n-tuple:
    # (CIRCLE, radius, color, lineWidth)
    # (RECTANGLE, width, height, color, lineWidth)
    # (POLYGON, points, color, lineWidth)
    # (LINE, points, color, lineWidth)
    # (TEXT, string, color, size)
    # (IMAGE, surface)          a png, jpg, etc
    # (PLACED, top, (x, y), bottom)
    #
    def render(display, imagesxy):
        while imagesxy != []:
            (image, x, y) = imagesxy.pop()

            typ = image[0]
            if typ == Shape.Circle:
                (_, radius, color, lineWidth) = image
                pygame.draw.circle(display, color, (x+radius, y+radius), radius, lineWidth)
            if typ == Shape.Rectangle:
                (_, width, height, color, lineWidth) = image
                pygame.draw.rect(display, color, (x, y, width, height), lineWidth)

            if typ == Shape.Line:
                (_, dxdys, color, lineWidth) = image

                # (xmin, ymin) displacements to upper left corner of
                # line's bounding box
                xmin = findMin([ dx for (dx, _) in dxdys])
                ymin = findMin([ dy for (_, dy) in dxdys])

                x0 = x if xmin >= 0 else x + abs(xmin)
                y0 = y if ymin >= 0 else y + abs(ymin)

                for (dx, dy) in dxdys:
                    x1, y1 = x0+dx, y0+dy
                    pygame.draw.line(display, color, (x0, y0), (x1, y1), lineWidth)
                    x0, y0 = x1, y1

            if typ == Shape.Placed:
                (_, top, (x0, y0), bottom) = image
                imagesxy.append((top, x0+x, y0+y))
                imagesxy.append((bottom, x, y))

            if typ == Shape.Polygon: # convert from displacements to points
                (_, dxdys, color, lineWidth) = image

                # (xmin, ymin) displacements to upper left corner of
                # polygon's bounding box
                xmin = findMin([ dx for (dx, _) in dxdys])
                ymin = findMin([ dy for (_, dy) in dxdys])

                x0 = x if xmin >= 0 else x + abs(xmin)
                y0 = y if ymin >= 0 else y + abs(ymin)

                points = [(x0, y0)]
                for (dx, dy) in dxdys:
                    x1, y1 = x0+dx, y0+dy
                    points.append((x1, y1))
                    x0, y0 = x1, y1
                pygame.draw.polygon(display, color, points, lineWidth)

            if typ == Shape.Text:
                (_, text, color, size) = image
                font = pygame.font.SysFont("Verdana", size)
                textSurface = font.render(text, True, color)
                display.blit(textSurface, (x, y))

            if typ == Shape.Image:
                (_, img) = image
                display.blit(img, (x, y))

    # The API
    #
    def circle(radius, color, lineWidth=0):
        return (Shape.Circle, radius, color, lineWidth)

    def line(points, color, lineWidth=1):
        return (Shape.Line, points, color, lineWidth)

    def polygon(points, color, lineWidth=0):
        return (Shape.Polygon, points, color, lineWidth)

    def rectangle(width, height, color, lineWidth=0):
        return (Shape.Rectangle, width, height, color, lineWidth)

    def empty(width, height, color):
        return Image.rectangle(width, height, color)

    def text(string, color, size=FONTSIZE):
        return (Shape.Text, string, color, size)

    def placeImage(top, xy, bottom):
        return (Shape.Placed, top, xy, bottom)

    def placeImages(tops, xys, bottom):
        if len(tops) != len(xys):
            raise Exception("placeImages: tops and xys don't match.")
        for i in range(len(tops)):
            top, xy = tops[i], xys[i]
            bottom = Image.placeImage(top, xy, bottom)
        return bottom

    # read : string -> image
    def read(path):
        return (Shape.Image, pygame.image.load(path))

    def dimensions(image):
        (_, img) = image
        return pygame.Surface.get_size(img)

    # toArray : surface -> 2D-array (numpy)
    def toArray(image):
        (_, img) = image
        return pygame.PixelArray.transpose(pygame.PixelArray(img))

    # arrayToImage : 2D-array -> surface NB: array can be either standard or numpy
    def fromArray(a):
        a = pygame.PixelArray.transpose(a)
        return (Shape.Image, pygame.PixelArray.make_surface(a))

# Default functions for the animation loop
empty = Image.empty(WIDTH, HEIGHT, Color.DarkGray)

def defaultView(model): return empty
def defaultTickUpdate(model): return model
def defaultTouchUpdate(model, xy, updown): return model
def defaultKeyUpdate(model, key): return model
def defaultStopWhen(model): return True
def defaultViewLast(model): return empty

class Animate():

    # Frames/second
    FPS = 30

    def start(model=None,
              title="CSCI 1100",
              width=WIDTH,
              height=HEIGHT,
              view=defaultView,               # model -> Image
              tickUpdate=defaultTickUpdate,   # model -> model
              touchUpdate=defaultTouchUpdate, # model * x * y * UP/DOWN -> model
              keyUpdate=defaultKeyUpdate,     # model * keyname -> model
              stopWhen=defaultStopWhen,       # model -> boolean
              viewLast=defaultViewLast,       # model -> Image
              rate=FPS):

        pygame.init()

        clock = pygame.time.Clock()

        display = pygame.display.set_mode((width, height))
        display.fill(Color.LightGray)
        pygame.display.set_caption(title)

        finished = stopWhen(model)

        while True:
            if not finished:
                image = view(model)
                Image.render(display, [(image, 0, 0)])   # (0, 0) upper left
                pygame.display.update()

                events = pygame.event.get()

                if events == []:
                    model = tickUpdate(model)
                else:
                    for event in events:
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONUP:
                            xy = pygame.mouse.get_pos()
                            model = touchUpdate(model, xy, Touch.Up)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            xy = pygame.mouse.get_pos()
                            model = touchUpdate(model, xy, Touch.Down)
                        if event.type == pygame.KEYDOWN:
                            keyname = pygame.key.name(event.key)
                            model = keyUpdate(model, keyname)                            
            
                clock.tick(rate)
                finished = stopWhen(model)
            else: 
                # All done
                image = viewLast(model)
                Image.render(display, [(image, 0, 0)])
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

    def show(path):
        image = Image.read(path)
        (width, height) = Image.dimensions(image)
        Animate.start(width  = width,
                      height = height,
                      viewLast = lambda _ : image,
                      stopWhen = lambda _ : True)
        
