import pygame
from math import *
from pygame.locals import *
import sys

pygame.init()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # set the display mode, window title and FPS clock
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

f = open('./map_data.txt', 'w')

map_data = [[[] for _ in range(1000)] for i in range(1000)]

BLOCKSIZE = 40
# tree1 = pygame.image.load('./img/tree1.png').convert_alpha()  # load images
# tree1 = pygame.transform.scale(tree1, (BLOCKSIZE, BLOCKSIZE))
# tree2 = pygame.image.load('./img/tree2.png').convert_alpha()  # load images
# tree2 = pygame.transform.scale(tree2, (BLOCKSIZE, BLOCKSIZE))
# tree3 = pygame.image.load('./img/tree3.png').convert_alpha()  # load images
# tree3 = pygame.transform.scale(tree3, (BLOCKSIZE, BLOCKSIZE))
ground = pygame.image.load('./img/ground.png').convert_alpha()  # load images
ground = pygame.transform.scale(ground, (BLOCKSIZE, BLOCKSIZE))
ground2 = pygame.image.load('./img/ground2.png').convert_alpha()  # load images
ground2 = pygame.transform.scale(ground2, (BLOCKSIZE, BLOCKSIZE))
# stone = pygame.image.load('./img/stone.png').convert_alpha()  # load images
# stone = pygame.transform.scale(stone, (BLOCKSIZE, BLOCKSIZE))

Blocks = []
for i in range(101):
    Blocks.append(pygame.image.load('./img/Blocks/blocks_'+str(i+1)+'.png').convert_alpha())
    Blocks[i] = pygame.transform.scale(Blocks[i], (BLOCKSIZE, BLOCKSIZE))


TILEWIDTH = BLOCKSIZE  # holds the tile width and height
TILEHEIGHT = BLOCKSIZE
TILEHEIGHT_HALF = TILEHEIGHT / 2
TILEWIDTH_HALF = TILEWIDTH / 2

RENDER = 70
def makescreen(posx, posy):
    map_data[int(posx)][int(posy)]=[0]
    DISPLAYSURF.fill((0,0,0))
    for row_nb in range(2*RENDER+1):
        for col_nb in range(2 * RENDER+1):
            cart_x = row_nb * TILEWIDTH_HALF
            cart_y = col_nb * TILEHEIGHT_HALF
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y) / 2
            centered_x = DISPLAYSURF.get_rect().centerx + iso_x
            centered_y = - RENDER * TILEWIDTH_HALF + iso_y + DISPLAYSURF.get_rect().centery*1.5
            if row_nb == checkx-nowx+RENDER and col_nb == checky-nowy+RENDER:
                DISPLAYSURF.blit(ground2, (centered_x - BLOCKSIZE / 2, centered_y - 3*BLOCKSIZE / 4))
            else:
                DISPLAYSURF.blit(ground, (centered_x - BLOCKSIZE / 2, centered_y - 3*BLOCKSIZE / 4))

    for i in range(2*RENDER+1):  # for every row of the map...
        if i + int(posx) - RENDER < 0 or i + int(posx) - RENDER >= len(map_data):
            continue
        for j in range(2*RENDER+1):
            if j + int(posy) - RENDER < 0 or j + int(posy) - RENDER >= len(map_data[0]):
                continue
            tile = map_data[i+int(posx)-RENDER][j+int(posy)-RENDER]
            cart_x = (i-posx+int(posx)) * TILEWIDTH_HALF
            cart_y = (j-posy+int(posy)) * TILEHEIGHT_HALF
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y) / 2
            centered_x = DISPLAYSURF.get_rect().centerx + iso_x
            for k, img in enumerate(tile):
                centered_y = -RENDER * TILEWIDTH_HALF + iso_y + DISPLAYSURF.get_rect().centery*1.5 - TILEHEIGHT_HALF * k
                DISPLAYSURF.blit(Blocks[img], (centered_x - BLOCKSIZE/2, centered_y - 3*BLOCKSIZE/4))  # display the actual tile
    pygame.draw.circle(DISPLAYSURF, (0, 0, 255), [DISPLAYSURF.get_rect().centerx, DISPLAYSURF.get_rect().centery*1.5], 1)

def getpos(a, b):
    posx, posy = DISPLAYSURF.get_rect().centerx, DISPLAYSURF.get_rect().centery*1.5
    alpha =  atan((posy - b) / (posx - a))
    if alpha < 0:
        alpha += pi
    if b > posy:
        alpha += pi
    d = sqrt((posx - a)**2+(posy - b)**2)
    theta = atan(1/2)
    x = floor(d*sin(alpha + theta) / ((BLOCKSIZE)/(2*cos(theta))) / sin(2*theta)  + 0.5)
    y = floor(d*sin(alpha - theta) / ((BLOCKSIZE)/(cos(theta)*2)) / sin(2*theta) + 0.5)
    return nowx - x, nowy - y

nowx = 300
nowy = 300
vx = 0
vy = 0
speed = 1
checkx = -1
checky = -1
blockidx = 0
makescreen(nowx, nowy)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == KEYDOWN or event.type == KEYUP:
            if event.key == K_UP:
                (vx, vy) = (vx - speed, vy - speed) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_LEFT:
                (vx, vy) = (vx - speed, vy + speed) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_DOWN:
                (vx, vy) = (vx + speed, vy + speed) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_RIGHT:
                vx, vy = (vx + speed, vy - speed) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_b and event.type == KEYUP:
                map_data[checkx][checky].append(blockidx)
            elif event.key == K_BACKSPACE and event.type == KEYUP and len(map_data[checkx][checky]) != 0:
                map_data[checkx][checky].pop()
            elif event.key == K_RETURN and event.type == KEYUP:
                blockidx += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            checkx, checky = getpos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    nowx += vx
    nowy += vy
    makescreen(nowx, nowy)

    pygame.display.flip()