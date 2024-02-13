import pygame
from math import *
from pygame.locals import *
import sys, pickle
import os

pygame.init()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # set the display mode, window title and FPS clock
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

with open('./map/map_data.pkl', 'rb') as f:
    map = pickle.load(f)

BLOCKSIZE = 5
# ground = pygame.image.load('./img/ground1.png').convert_alpha()  # load images
# ground = pygame.transform.scale(ground, (BLOCKSIZE, BLOCKSIZE))
# ground2 = pygame.image.load('./img/ground2.png').convert_alpha()  # load images
# ground2 = pygame.transform.scale(ground2, (BLOCKSIZE, BLOCKSIZE))
showblockidx = pygame.image.load('./img/showblockidx.png').convert_alpha()
showblockidx = pygame.transform.scale(showblockidx, (120, 120))
grid = pygame.image.load('./img/grid.png').convert_alpha()
grid = pygame.transform.scale(grid, (BLOCKSIZE, BLOCKSIZE))
activate = pygame.image.load('./img/activate.png').convert_alpha()
activate = pygame.transform.scale(activate, (BLOCKSIZE, BLOCKSIZE))

Blocks = []


def get_files_count(folder_path):
    dirListing = os.listdir(folder_path)
    return len(dirListing)


Blocknum = get_files_count('./img/Blocks')

for i in range(Blocknum):
    Blocks.append(pygame.image.load('./img/Blocks/blocks_' + str(i + 1) + '.png').convert_alpha())
    Blocks[i] = pygame.transform.scale(Blocks[i], (BLOCKSIZE, BLOCKSIZE))

HALF = BLOCKSIZE / 2

RENDER = 150
flip = 0
mul = 1

def makescreen(posx, posy):
    DISPLAYSURF.fill((0, 128, 0))
    if flip == 0:
        activate_coordi = (DISPLAYSURF.get_rect().centerx + HALF * (checkx1 - nowx - checky1 + nowy) -
                       BLOCKSIZE / 2, HALF * (checkx1 - nowx + checky1 - nowy) / 2 +
                       DISPLAYSURF.get_rect().centery * 1.5 - 3 * BLOCKSIZE / 4)[:]
    else:
        activate_coordi = (DISPLAYSURF.get_rect().centerx + HALF * (-checkx1 + nowx + checky1 - nowy) -
                           BLOCKSIZE / 2, HALF * (-checkx1 + nowx  - checky1 + nowy) / 2 +
                           DISPLAYSURF.get_rect().centery * 1.5 - 3 * BLOCKSIZE / 4)[:]

    for i in range(2 * RENDER + 1):  # for every row of the map...
        if i + int(posx) - RENDER < 0 or i + int(posx) - RENDER >= len(map):
            continue
        for j in range(2 * RENDER + 1):
            if j + int(posy) - RENDER < 0 or j + int(posy) - RENDER >= len(map[0]):
                continue
            if flip == 0:
                tile = map[i + int(posx) - RENDER][j + int(posy) - RENDER]
            else:
                tile = map[2 * int(posx)- (i + int(posx) - RENDER)][2 * int(posy) - (j + int(posy) - RENDER)]
            cart_x = (i - posx + int(posx)) * HALF
            cart_y = (j - posy + int(posy)) * HALF
            # iso_x = (cart_x - cart_y)
            # iso_y = (cart_x + cart_y) / 2
            centered_x = DISPLAYSURF.get_rect().centerx + cart_x
            for img in tile:
                # centered_y = -RENDER * HALF + cart_y + DISPLAYSURF.get_rect().centery * 1.5 - HALF * img[1]
                centered_y = cart_y
                DISPLAYSURF.blit(Blocks[img[0]], (centered_x - BLOCKSIZE / 2, centered_y - 3 * BLOCKSIZE / 4))  # display the actual tile
    if activate_coordi: DISPLAYSURF.blit(activate, activate_coordi)



def getpos(a, b):
    posx, posy = DISPLAYSURF.get_rect().centerx, DISPLAYSURF.get_rect().centery * 1.5
    if posx != a:
        alpha = atan((posy - b) / (posx - a))
    else:
        alpha = pi / 2
    if alpha < 0:
        alpha += pi
    if b > posy:
        alpha += pi
    d = sqrt((posx - a) ** 2 + (posy - b) ** 2)
    theta = atan(1 / 2)
    x = floor(d * sin(alpha + theta) / ((BLOCKSIZE) / (2 * cos(theta))) / sin(2 * theta) + 0.5)
    y = floor(d * sin(alpha - theta) / ((BLOCKSIZE) / (cos(theta) * 2)) / sin(2 * theta) + 0.5)
    if flip == 0:
        return nowx - x, nowy - y
    else:
        return nowx+x, nowy+y


def text(s, size, x, y):
    font = pygame.font.Font(None, size)
    text = font.render(str(s), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.left = x
    textRect.top = y
    DISPLAYSURF.blit(text, textRect)

nowx = 300
nowy = 300
vx = 0
vy = 0
speed = 1
checkx1 = -1
checky1 = -1
blockidx = 0
det = 0
height = 1
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
            if event.key == K_w:
                (vx, vy) = (vx - speed*mul, vy - speed*mul) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_a:
                (vx, vy) = (vx - speed*mul, vy + speed*mul) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_s:
                (vx, vy) = (vx + speed*mul, vy + speed*mul) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_d:
                (vx, vy) = (vx + speed*mul, vy - speed*mul) if event.type == KEYDOWN else (0, 0)
            elif event.key == K_UP and event.type == KEYUP and det == 0:
                det = 1
            elif event.key == K_LEFT and event.type == KEYUP and det == 0:
                det = 2
            elif event.key == K_DOWN and event.type == KEYUP and det == 0:
                det = 3
            elif event.key == K_RIGHT and event.type == KEYUP and det == 0:
                det = 4
            elif event.key == K_SPACE and event.type == KEYUP:
                last = 0
                if len(map[checkx1][checky1])!=0:
                    last = map[checkx1][checky1][-1][1]+1
                map[checkx1][checky1].extend([(blockidx, last+i) for i in range(height)])
            elif event.key == K_BACKSPACE and event.type == KEYDOWN:
                for i in range(height):
                    if len(map[checkx1][checky1]) != 0:
                        map[checkx1][checky1].pop()
            elif event.key == K_PERIOD and event.type == KEYUP:
                blockidx += 1
            elif event.key == K_COMMA and event.type == KEYUP:
                blockidx -= 1
            elif event.key == K_f and event.type == KEYUP:
                flip = 1 - flip
            elif event.key == K_c and event.type == KEYUP:
                height = int(input("Enter: "))
            elif event.key == K_e and event.type == KEYUP:
                map[checkx1][checky1] = map[checkx1][checky1][height:]
            elif event.key == K_DELETE and event.type == KEYUP:
                map[checkx1][checky1].clear()

            elif event.key == K_NUMLOCK and event.type == KEYUP:
                pygame.quit()
                sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            checkx1, checky1 = getpos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            print(checkx1, checky1)

        # if event.type == pygame.MOUSEWHEEL:
        #     BLOCKSIZE += 30 * event.y

        if flip: mul=-1
        else:
            mul = 1

        if det == 1:
            checky1 -= mul
            det = 0
        elif det == 2:
            checkx1 -= mul
            det = 0
        elif det == 3:
            checky1 += mul
            det = 0
        elif det == 4:
            checkx1 += mul
            det = 0

        if blockidx == -1:
            blockidx = Blocknum - 1
        elif blockidx == Blocknum:
            blockidx = 0

    nowx += vx
    nowy += vy
    makescreen(nowx, nowy)


    pygame.display.flip()