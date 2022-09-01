from animate import *
import sys, pygame

pygame.init()

image = pygame.image.load("./pots.png")
dimensions = pygame.Surface.get_size(image)
cols, rows = dimensions[0], dimensions[1]   # width x height
print(f'image surface has {rows} rows and {cols} colulumns')
image_rect = image.get_rect()
print(f'image rect is {image_rect}')

screen = pygame.display.set_mode(dimensions)
screen.fill((0,0,127))
screen.blit(image, image_rect)
screensurf = pygame.display.get_surface()

while 1:

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN :
            pxarray = pygame.PixelArray(image) # screensurf)
            (col, row) = pygame.mouse.get_pos()
            item = pxarray[col, row]
            print(f'the item in [{col}, {row}] is {item}')
            whozee = pygame.Color(item)
            print(f'pygame.Color of that is {whozee}')

            # (col, row) = mouse
            print(f'touch at row {row} and col {col}')
            for r in range(10):
                for c in range(10):
                    pxarray[col+c][row+r] = pygame.Color(255, 255, 255)
            image = pygame.PixelArray.make_surface(pxarray)
            screen.blit(image, image_rect)
            pixel = pygame.Color(pxarray[col,row])
            print(pixel)
            print(screensurf.get_at((col, row)))
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
