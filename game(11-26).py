import pygame
from math import *
from pygame.locals import *
import sys
import pickle
import os

BLOCKSIZE = 55
HALF = BLOCKSIZE / 2
RENDER = 65

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

center_coordi = (DISPLAYSURF.get_rect().centerx, DISPLAYSURF.get_rect().centery)


def get_files_count(folder_path):
    dirlisting = os.listdir(folder_path)
    return len(dirlisting)


showblockidx = pygame.image.load('./img/showblockidx.png').convert_alpha()
showblockidx = pygame.transform.scale(showblockidx, (120, 120))
activate = pygame.image.load('./img/activate.png').convert_alpha()
activate = pygame.transform.scale(activate, (BLOCKSIZE, BLOCKSIZE))
start_img = pygame.image.load('./img/start_img.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))

button_scale = (200, 100)
play_img = pygame.image.load('./img/play.png').convert_alpha()
play_img = pygame.transform.scale(play_img, button_scale)
rect_play = pygame.Rect(play_img.get_rect())
tutorial_img = pygame.image.load('./img/tutorial.png').convert_alpha()
tutorial_img = pygame.transform.scale(tutorial_img, button_scale)
rect_tutorial = pygame.Rect(tutorial_img.get_rect())



Blocks = []
Blocknum = get_files_count('./img/Blocks')
humanImage = pygame.transform.scale(pygame.image.load('./img/human.png').convert_alpha(), (55, 132))
for i in range(Blocknum):
    Blocks.append(pygame.image.load('./img/Blocks/blocks_' + str(i + 1) + '.png').convert_alpha())
    Blocks[i] = pygame.transform.scale(Blocks[i], (BLOCKSIZE, BLOCKSIZE))


class Screen:
    def __init__(self, name):
        self.name = name
        with open(name, 'rb') as f:
            self.map_data = pickle.load(f)
        self.activatex1, self.activatey1 = -1, -1
        self.posx, self.posy = 300, 300
        self.height = 1
        self.blockidx = 0
        self.flip = 1
        self.items = []
        self.Blocknum = 0

    def makescreen(self):
        DISPLAYSURF.fill((0, 128, 0))

        for item in self.items:
            if item.coorx != -1:
                tile = self.map_data[item.coorx][item.coory]
                if len(tile) != 0:
                    height = max(tile, key=lambda x: x[1])[1]
                else:
                    height = -1
                cart_x = (item.coorx - self.posx) * HALF * self.flip
                cart_y = (item.coory - self.posy) * HALF * self.flip
                iso_x = (cart_x - cart_y)
                iso_y = (cart_x + cart_y) / 2
                centered_x = DISPLAYSURF.get_rect().centerx + iso_x
                centered_y = iso_y + DISPLAYSURF.get_rect().centery * 1.5 - HALF * (height + 1)
                item.itemrect.left = centered_x - item.standard[0]
                item.itemrect.top = centered_y - item.standard[1]
                DISPLAYSURF.blit(item.image, item.itemrect)

        if self.flip == 1:
            activate_coordi = (DISPLAYSURF.get_rect().centerx + HALF * (
                        self.activatex1 - self.posx - self.activatey1 + self.posy) -
                               BLOCKSIZE / 2, HALF * (self.activatex1 - self.posx + self.activatey1 - self.posy) / 2 +
                               DISPLAYSURF.get_rect().centery * 1.5 - 3 * BLOCKSIZE / 4)[:]
        else:
            activate_coordi = (DISPLAYSURF.get_rect().centerx + HALF * (
                        - self.activatex1 + self.posx + self.activatey1 - self.posy) -
                               BLOCKSIZE / 2, HALF * (-self.activatex1 + self.posx - self.activatey1 + self.posy) / 2 +
                               DISPLAYSURF.get_rect().centery * 1.5 - 3 * BLOCKSIZE / 4)[:]

        for i in range(2 * RENDER + 1):
            if i + int(self.posx) - RENDER < 0 or i + int(self.posx) - RENDER >= len(self.map_data):
                continue
            for j in range(2 * RENDER + 1):
                if j + int(self.posy) - RENDER < 0 or j + int(self.posy) - RENDER >= len(self.map_data[0]):
                    continue
                if abs((i - j) * HALF) > DISPLAYSURF.get_rect().centerx:
                    continue
                if -RENDER * HALF + (
                        i + j) * HALF / 2 + DISPLAYSURF.get_rect().centery * 1.5 - HALF * 50 > 2 * DISPLAYSURF.get_rect().centery:
                    continue
                if -RENDER * HALF + (i + j) * HALF / 2 + DISPLAYSURF.get_rect().centery * 1.5 < 0:
                    continue
                if self.flip == 1:
                    tile = self.map_data[i + self.posx - RENDER][j + self.posy - RENDER]
                else:
                    tile = self.map_data[2 * self.posx - (i + self.posx - RENDER)][
                        2 * self.posy - (j + self.posy - RENDER)]
                cart_x = i * HALF
                cart_y = j * HALF
                iso_x = (cart_x - cart_y)
                iso_y = (cart_x + cart_y) / 2
                centered_x = DISPLAYSURF.get_rect().centerx + iso_x
                for img in tile:
                    centered_y = -RENDER * HALF + iso_y + DISPLAYSURF.get_rect().centery * 1.5 - HALF * img[1]
                    DISPLAYSURF.blit(Blocks[img[0]], (
                        centered_x - BLOCKSIZE / 2, centered_y - 3 * BLOCKSIZE / 4))  # display the actual tile
                if i == RENDER and j == RENDER:
                    tile = self.map_data[self.posx][self.posy]
                    if len(tile) != 0:
                        height = max(tile, key=lambda x: x[1])[1]
                    else:
                        height = -1
                    DISPLAYSURF.blit(humanImage, (DISPLAYSURF.get_rect().centerx-humanImage.get_width()/2,
                                                  DISPLAYSURF.get_rect().centery * 1.5 - HALF * (height + 1)
                                                  - humanImage.get_height()))

        if activate_coordi: DISPLAYSURF.blit(activate, activate_coordi)
        DISPLAYSURF.blit(showblockidx,
                         (DISPLAYSURF.get_rect().centerx + 610, DISPLAYSURF.get_rect().centery - 390))
        self.text(f'{self.blockidx}', 30, DISPLAYSURF.get_rect().centerx + 685, DISPLAYSURF.get_rect().centery - 375)
        DISPLAYSURF.blit(Blocks[self.blockidx],
                         (DISPLAYSURF.get_rect().centerx + 650, DISPLAYSURF.get_rect().centery - 350))

    def coordinate(self, a, b):
        centerx, centery = DISPLAYSURF.get_rect().centerx, DISPLAYSURF.get_rect().centery * 1.5
        if centerx != a:
            alpha = atan((centery - b) / (centerx - a))
        else:
            alpha = pi / 2
        if alpha < 0:
            alpha += pi
        if b > centery:
            alpha += pi
        d = sqrt((centerx - a) ** 2 + (centery - b) ** 2)
        theta = atan(1 / 2)
        x = floor(d * sin(alpha + theta) / ((BLOCKSIZE) / (2 * cos(theta))) / sin(2 * theta) + 0.5)
        y = floor(d * sin(alpha - theta) / ((BLOCKSIZE) / (cos(theta) * 2)) / sin(2 * theta) + 0.5)
        if self.flip == 1:
            return self.posx - x, self.posy - y
        else:
            return self.posx + x, self.posy + y

    def build(self):
        last = 0
        if len(self.map_data[self.activatex1][self.activatey1]) != 0:
            last = self.map_data[self.activatex1][self.activatey1][-1][1] + 1
        self.map_data[self.activatex1][self.activatey1].extend([(self.blockidx, last + i) for i in range(self.height)])

    def erase(self):
        self.map_data[self.activatex1][self.activatey1] = self.map_data[self.activatex1][self.activatey1][self.height:]

    def delete(self):
        for i in range(self.height):
            if len(self.map_data[self.activatex1][self.activatey1]) != 0:
                self.map_data[self.activatex1][self.activatey1].pop()

    def click(self, a, b):
        coord = self.coordinate(a, b)
        print(coord)
        print(coord)
        self.activatex1, self.activatey1 = coord[0], coord[1]

    def move(self, a, b):
        global screen
        idx = 0
        for i in range(6):
            if screen == screens[i]:
                idx = i
        if idx == 0 and 292 <= self.posx <= 308 and 283 <= self.posy <= 286 and len(self.map_data[self.posx][self.posy]) != 0:
            screen = screens[1]
            screen.posx = 301
            screen.posy = 350
            screen.flip = self.flip
        if idx == 0 and self.posy == 245 and 288 <= self.posx <= 294 and len(self.map_data[self.posx][self.posy]) == 0:
            screen = screens[1]
            screen.posx = 275
            screen.posy = 251
            screen.flip = self.flip
        if idx == 0 and self.posy == 245 and 306 <= self.posx <= 312 and len(self.map_data[self.posx][self.posy]) == 0:
            screen = screens[1]
            screen.posx = 320
            screen.posy = 252
            screen.flip = self.flip
        if idx == 1 and 249 <= self.posy <= 250 and 271 <= self.posx <= 329:
            screen = screens[0]
            screen.posx = 300
            screen.posy = 243
            screen.flip = -1
        if idx == 1 and 284 <= self.posx <= 315 and self.posy == 258:
            screen = screens[2]
            screen.posx = 278
            screen.posy = 261
            screen.flip = - self.flip
        for i in range(2, 5):
            if idx == i and 284 <= self.posx <= 315 and self.posy == 258:
                screen = screens[i+1]
                screen.posx = 278
                screen.posy = 261
                screen.flip = - self.flip
            if idx == i and 257 <= self.posy <= 258 and (271 <= self.posx <= 283 or 316 <= self.posx <= 329):
                screen = screens[i-1]
                screen.posx = 298
                screen.posy = 260
                screen.flip = - self.flip

        if len(self.map_data[self.posx][self.posy]) == 0:
            t1 = 0
        else:
            t1 = max(self.map_data[self.posx][self.posy], key=lambda x:x[1])[1]
        if len(self.map_data[self.posx + a * self.flip][self.posy + b * self.flip]) == 0:
            t2 = 0
        else:
            t2 = max(self.map_data[self.posx + a * self.flip][self.posy + b * self.flip], key=lambda x:x[1])[1]
        if len(self.map_data[self.posx + a * self.flip // 2][self.posy + b * self.flip // 2]) == 0:
            t3 = 0
        else:
            t3 = max(self.map_data[self.posx + a * self.flip // 2][self.posy + b * self.flip // 2], key=lambda x: x[1])[1]
        sub = max(abs(t2 - t1), abs(t3 - t1))
        if sub == 0:
            self.posx += a * self.flip
            self.posy += b * self.flip


    def move_block(self, a, b):
        self.activatex1 += a * self.flip
        self.activatey1 += b * self.flip

    def fflip(self):
        self.flip = -self.flip

    def text(self, s, size, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(str(s), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.left = x
        textRect.top = y
        DISPLAYSURF.blit(text, textRect)

    def save(self):
        with open(self.name, 'wb') as f:
            pickle.dump(self.map_data, f, protocol=pickle.HIGHEST_PROTOCOL)

    def getheight(self):
        self.height = int(input("Enter: "))

    def changeblock(self, t):
        self.blockidx += t
        if self.blockidx == -1:
            self.blockidx = self.Blocknum - 1
        elif self.blockidx == self.Blocknum:
            self.blockidx = 0

    def pos_absolute_center(self, img, x=-1, y=-1, mode=1):
        if x == -1:
            x = DISPLAYSURF.get_rect().centerx
        if y == -1:
            y = DISPLAYSURF.get_rect().centery
        if mode == 1:
            DISPLAYSURF.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))
        else:
            DISPLAYSURF.blit(img, (x, y))


class Human():
    def __init__(self):
        self.bag = []
        self.grabbing = NoItem
        self.chessImage = pygame.transform.scale(pygame.image.load('./img/chessImage.png').convert_alpha(), (909 * 55 / 55.5, 618 * 55 / 55.5))

    def showing_bag(self):
        screen.pos_absolute_center(self.chessImage)
        print(DISPLAYSURF.get_rect().centerx - self.chessImage.get_width() / 2, DISPLAYSURF.get_rect().centery - self.chessImage.get_height() / 2)
        for i, item in enumerate(self.bag):
            l = i % 13
            r = i // 13
            screen.pos_absolute_center(item.image, DISPLAYSURF.get_rect().centerx-864+507 + 55 * l, DISPLAYSURF.get_rect().centery-540+320 + 55 * r, 0)
        human.get_item()

    def get_item(self):
        flag = 0
        pygame.display.flip()
        while True:
            if flag == 1:
                break
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    stx = DISPLAYSURF.get_rect().centerx-864+507
                    sty = DISPLAYSURF.get_rect().centery-540+320
                    print(stx, sty, x, y)
                    print(DISPLAYSURF.get_rect())

                    if x < stx or x > stx + 55 * 13 or y < sty or y > sty + 55 * 8:
                        self.grabbing = NoItem
                        flag = 1
                        break
                    i = (x - stx) // 55
                    j = (y - sty) // 55
                    idx = i + 13 * j
                    if idx < len(self.bag):
                        self.grabbing = self.bag[idx]
                    else:
                        self.grabbing = NoItem
                    flag = 1
                    break

    def grab(self):
        if self.grabbing == NoItem:
            return
        else:
            screen.pos_absolute_center(self.grabbing.image, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

    def click(self, x, y):
        if self.grabbing == NoItem:
            for item in screen.items:
                if item.itemrect.left <= x <= item.itemrect.right and item.itemrect.top <= y <= item.itemrect.bottom:
                    screen.items.remove(item)
                    if type(item) not in self.bag:
                        self.bag.append(type(item))
        else:
            a, b = screen.coordinate(x, y + self.grabbing.image.get_rect().height / 2)
            new_item = self.grabbing(a, b)
            screen.items.append(new_item)


class Item():
    def __init__(self, a=-1, b=-1, c=-1, d=-1, L=None):
        if L is None:
            L = []
        self.coorx = a
        self.coory = b
        self.environment = L
        self.standard = (c, d)

    def activate(self):
        for env in self.environment:
            if [self.coorx, self.coory] in []:
                pass


class Bottle(Item):
    image = pygame.transform.scale(pygame.image.load('./img/Items/bottle.png'), (55, 55))

    def __init__(self, a, b):
        super().__init__(a, b, 55 // 2, 55)
        self.itemrect = pygame.Rect(Bottle.image.get_rect())


class Axe(Item):
    image = pygame.transform.scale(pygame.image.load('./img/Items/axe.png'), (55, 55))

    def __init__(self, a, b):
        super().__init__(a, b, 55 // 2, 55 // 2)
        self.itemrect = pygame.Rect(Axe.image.get_rect())


class NoItem(Item):
    image = None


pygame.init()
bottle = Bottle(290, 300)
axe = Axe(300, 300)
screens = [Screen('./map/map_data.pkl'), Screen('./map/floor_1.pkl'), Screen('./map/floor_2.pkl'), Screen('./map/floor_3.pkl'),
           Screen('./map/floor_4.pkl'), Screen('./map/rooftop.pkl')]
screens[0].items.extend([bottle, axe])
screen = screens[0]
human = Human()


def game():
    startfpsClock = pygame.time.Clock()

    vx = 0
    vy = 0
    speed = 1
    mode = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN or event.type == KEYUP:
                if event.key == K_w:
                    (vx, vy) = (vx - speed, vy - speed) if event.type == KEYDOWN else (0, 0)
                elif event.key == K_a:
                    (vx, vy) = (vx - speed, vy + speed) if event.type == KEYDOWN else (0, 0)
                elif event.key == K_s:
                    (vx, vy) = (vx + speed, vy + speed) if event.type == KEYDOWN else (0, 0)
                elif event.key == K_d:
                    (vx, vy) = (vx + speed, vy - speed) if event.type == KEYDOWN else (0, 0)

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    screen.save()
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    screen.move_block(0, -1)
                elif event.key == K_DOWN:
                    screen.move_block(0, 1)
                elif event.key == K_LEFT:
                    screen.move_block(-1, 0)
                elif event.key == K_RIGHT:
                    screen.move_block(1, 0)
                elif event.key == K_SPACE:
                    screen.build()
                elif event.key == K_BACKSPACE:
                    screen.delete()
                elif event.key == K_e:
                    screen.erase()
                elif event.key == K_f:
                    screen.fflip()
                elif event.key == K_PERIOD:
                    screen.changeblock(1)
                elif event.key == K_COMMA:
                    screen.changeblock(-1)
                elif event.key == K_c:
                    screen.getheight()
                elif event.key == K_b:
                    human.showing_bag()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == 1:
                    screen.click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                else:
                    human.click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        screen.move(vx, vy)
        screen.makescreen()
        human.grab()
        pygame.display.flip()

# print(rect_tutorial, rect_play)


def startgame():
    while True:
        DISPLAYSURF.blit(start_img, (0, 0))
        DISPLAYSURF.blit(tutorial_img, (center_coordi[0]+430, center_coordi[1]-180))
        DISPLAYSURF.blit(play_img, (center_coordi[0]+430, center_coordi[1]+120))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                startx1, starty1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                if (rect_tutorial.left <= startx1 <= rect_tutorial.right) and (rect_tutorial.top <= starty1 <= rect_tutorial.bottom):
                    print("tutorial pressed")
                if (rect_play.left <= startx1 <= rect_play.right) and (rect_play.top <= starty1 <= rect_play.bottom):
                    print("play pressed")
                    game()
            # if event.type == KEYDOWN or event.type == KEYUP:
            #     if event.key == 
        
        pygame.display.flip()
        
startgame()