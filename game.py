import pygame
from math import *
from pygame.locals import *
import sys
import pickle
import os
import random

BLOCKSIZE = 55
HALF = BLOCKSIZE / 2
RENDER = 65

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
fpsClock = pygame.time.Clock()
FPS = 30
pygame.init()
gamestarttime = 0
endtime = 0
inputidstr = 'unknown'
idtime = []
showhelp = -1
stage = 1
complete_time = -100
stage_end = 0


def get_files_count(folder_path):
    dirlisting = os.listdir(folder_path)
    return len(dirlisting)

activate = pygame.image.load('./img/activate.png').convert_alpha()
activate = pygame.transform.scale(activate, (BLOCKSIZE, BLOCKSIZE))
inputpassword = pygame.transform.scale(pygame.image.load('./img/inputpassword.png').convert_alpha(), (300, 100))
Blocks = []
Blocknum = get_files_count('./img/Blocks')
human1 = pygame.transform.scale(pygame.image.load('img/human1.png').convert_alpha(), (55, 132))
human2 = pygame.transform.scale(pygame.image.load('img/human2.png').convert_alpha(), (55, 132))
humanImage = human1
for i in range(Blocknum):
    Blocks.append(pygame.image.load('./img/Blocks/blocks_' + str(i + 1) + '.png').convert_alpha())
    Blocks[i] = pygame.transform.scale(Blocks[i], (BLOCKSIZE, BLOCKSIZE))

button_scale = (160, 100)
play_img = pygame.image.load('./img/play.png').convert_alpha()
play_img = pygame.transform.scale(play_img, button_scale)
rect_play = play_img.get_rect()
tutorial_img = pygame.image.load('./img/tutorial.png').convert_alpha()
tutorial_img = pygame.transform.scale(tutorial_img, button_scale)
rect_tutorial = tutorial_img.get_rect()
tuto_img = pygame.transform.scale(pygame.image.load('./img/tuto.png').convert_alpha(),
                                  (DISPLAYSURF.get_height(), DISPLAYSURF.get_height()))
start_img = pygame.image.load('./img/start_img.png').convert_alpha()
start_img = pygame.transform.scale(start_img, (DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))
end_img = pygame.transform.scale(pygame.image.load('./img/end_img.png').convert_alpha(),
                                 (DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))
c1 = pygame.transform.scale(pygame.image.load('./img/complete1.png').convert_alpha(), (100, 100))
c2 = pygame.transform.scale(pygame.image.load('./img/complete2.png').convert_alpha(), (100, 100))
c3 = pygame.transform.scale(pygame.image.load('./img/complete3.png').convert_alpha(), (100, 100))
c4 = pygame.transform.scale(pygame.image.load('./img/complete4.png').convert_alpha(), (100, 100))
c5 = pygame.transform.scale(pygame.image.load('./img/complete5.png').convert_alpha(), (100, 100))
clist = [c1, c2, c3, c4, c5]

m0 = pygame.transform.scale(pygame.image.load('img/minimap_0.png').convert_alpha(), (300, 300))
m1 = pygame.transform.scale(pygame.image.load('img/minimap_2.png').convert_alpha(), (300, 100))
m2 = pygame.transform.scale(pygame.image.load('img/minimap_1.png').convert_alpha(), (300, 100))
m5 = pygame.transform.scale(pygame.image.load('img/minimap_5.png').convert_alpha(), (300, 100))
mlist = [m0, m1, m2, m2, m2, m5]

reddot = pygame.transform.scale(pygame.image.load('./img/reddot.png').convert_alpha(), (10, 10))

inputidimg = pygame.transform.scale(pygame.image.load('./img/inputidimg.png').convert_alpha(),
                                    (DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))

you = pygame.transform.scale(pygame.image.load('./img/you.png').convert_alpha(), (50, 35))

helpimg1 = pygame.transform.scale(pygame.image.load('./img/helpimg1.png').convert_alpha(),
                                  (DISPLAYSURF.get_height(), DISPLAYSURF.get_height()))
helpimg2 = pygame.transform.scale(pygame.image.load('./img/helpimg2.png').convert_alpha(),
                                  (DISPLAYSURF.get_height(), DISPLAYSURF.get_height()))

center_coordi = (DISPLAYSURF.get_rect().centerx, DISPLAYSURF.get_rect().centery)

lefttop = pygame.transform.scale(pygame.image.load('./img/lefttop.png').convert_alpha(), (300, 100))
bgm_home = pygame.mixer.Sound("./audio/home.mp3")
bgm_stage1 = pygame.mixer.Sound("./audio/m1.mp3")
bgm_stage2 = pygame.mixer.Sound("./audio/m2.mp3")


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
        self.items = dict()
        self.environments = dict()
        self.npcs = []
        self.Blocknum = 0
        self.complete_num = 0
        self.cplt_img = clist[0]
        self.realx = center_coordi[0]
        self.realy = center_coordi[1] * 1.5

    idx = 0

    def makescreen(self):
        global showhelp, stage
        tile = self.map_data[self.posx][self.posy]
        if len(tile) != 0:
            height = max(tile, key=lambda x: x[1])[1]
        else:
            height = -1
        self.realx = center_coordi[0]
        self.realy = center_coordi[1] * 1.5 - HALF * (height + 1)
        DISPLAYSURF.fill((0, 128, 0))
        dic = dict()

        for idx, env in self.environments.items():
            dic[(idx[0] + env.r * self.flip, idx[1] + env.r * self.flip)] = env
        for i in range(2 * RENDER + 1):
            if i + int(self.posx) - RENDER < 0 or i + int(self.posx) - RENDER >= len(self.map_data):
                continue
            for j in range(2 * RENDER + 1):
                if j + int(self.posy) - RENDER < 0 or j + int(self.posy) - RENDER >= len(self.map_data[0]):
                    continue
                if abs((i - j) * HALF) > center_coordi[0]:
                    continue
                if -RENDER * HALF + (
                        i + j) * HALF / 2 + center_coordi[1] * 1.5 - HALF * 50 > 2 * center_coordi[1]:
                    continue
                if -RENDER * HALF + (i + j) * HALF / 2 + center_coordi[1] * 1.5 < 0:
                    continue

                if self.flip == 1:
                    x, y = i + self.posx - RENDER, j + self.posy - RENDER
                else:
                    x, y = 2 * self.posx - (i + self.posx - RENDER), 2 * self.posy - (j + self.posy - RENDER)
                tile = self.map_data[x][y]
                cart_x = i * HALF
                cart_y = j * HALF
                iso_x = (cart_x - cart_y)
                iso_y = (cart_x + cart_y) / 2
                centered_x = center_coordi[0] + iso_x
                for img in tile:
                    if img[0] == 103 and waterflag == 0: continue
                    centered_y = -RENDER * HALF + iso_y + center_coordi[1] * 1.5 - HALF * img[1]
                    DISPLAYSURF.blit(Blocks[img[0]], (
                        centered_x - BLOCKSIZE / 2, centered_y - 3 * BLOCKSIZE / 4))
                if i == RENDER and j == RENDER:

                    if self.complete_num:
                        self.cplt_img = clist[self.complete_num - 1]
                        DISPLAYSURF.blit(self.cplt_img,
                                         (self.realx - self.cplt_img.get_width() / 2,
                                          self.realy - self.cplt_img.get_height() + 50))

                    DISPLAYSURF.blit(humanImage, (center_coordi[0] - humanImage.get_width() / 2,
                                                  center_coordi[1] * 1.5 - HALF * (height + 1)
                                                  - humanImage.get_height()))
                if (x - 3 * self.flip, y - 3 * self.flip) in self.items.keys():
                    item = self.items[(x - 3 * self.flip, y - 3 * self.flip)]
                    tile = self.map_data[x - 3 * self.flip][y - 3 * self.flip]
                    if item.coorx != -1:
                        if len(tile) != 0:
                            height = max(tile, key=lambda x: x[1])[1]
                        else:
                            height = -1
                        cart_x = (item.coorx - self.posx) * HALF * self.flip
                        cart_y = (item.coory - self.posy) * HALF * self.flip
                        iso_x = (cart_x - cart_y)
                        iso_y = (cart_x + cart_y) / 2
                        centered_x = center_coordi[0] + iso_x
                        centered_y = iso_y + center_coordi[1] * 1.5 - HALF * (height + 1)
                        item.itemrect.left = centered_x - item.standard[0]
                        item.itemrect.top = centered_y - item.standard[1]
                        DISPLAYSURF.blit(item.image, item.itemrect)
                if (x, y) in dic.keys():
                    env = dic[(x, y)]
                    cart_x = (env.coorx - self.posx) * HALF * self.flip
                    cart_y = (env.coory - self.posy) * HALF * self.flip
                    iso_x = (cart_x - cart_y)
                    iso_y = (cart_x + cart_y) / 2
                    centered_x = center_coordi[0] + iso_x
                    centered_y = iso_y + center_coordi[1] * 1.5

                    env.envrect.left = centered_x - env.envrect.width / 2
                    env.envrect.top = centered_y - env.envrect.height
                    DISPLAYSURF.blit(env.img, env.envrect)

        for npc in self.npcs:
            if -5 <= npc.coorx - self.posx <= 5 and -5 <= npc.coory - self.posy <= 5:
                npc.talk()
        pygame.draw.circle(DISPLAYSURF, (255, 112, 18), (screen.realx, screen.realy - humanImage.get_height() / 2), 300,
                           10)
        self.minimap()

        DISPLAYSURF.blit(lefttop, (10, 10))

        self.text(f'time : {(pygame.time.get_ticks() - gamestarttime) // 1000}', 30, 20, 20)
        self.text(f'stage{stage}', 30, 20, 50)
        self.text(f'id:{inputidstr}', 30, 20, 80)

        if showhelp == 1:
            if stage == 1:
                helpimg = helpimg1
            else:
                helpimg = helpimg2
            DISPLAYSURF.blit(helpimg, (DISPLAYSURF.get_rect().centerx - DISPLAYSURF.get_height() / 2, 0))

    def coordinate(self, a, b):
        centerx, centery = center_coordi[0], center_coordi[1] * 1.5
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

    def click(self, a, b):
        coord = self.coordinate(a, b)
        self.activatex1, self.activatey1 = coord[0], coord[1]

    def move(self, a, b):
        global screen
        global idx
        idx = 0
        for i in range(6):
            if screen == screens[i]:
                idx = i
        for door in doors:
            door.move(idx, self.posx, self.posy)
        for env in self.environments.values():
            cart_x = (env.coorx - (self.posx + a * self.flip)) * HALF * self.flip
            cart_y = (env.coory - (self.posy + b * self.flip)) * HALF * self.flip
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y) / 2
            centered_x = center_coordi[0] + iso_x
            centered_y = iso_y + center_coordi[1] * 1.5
            l = centered_x - env.envrect.width / 2
            t = centered_y - env.envrect.height
            if l <= screen.realx <= l + env.img.get_rect().width and t <= screen.realy <= t + env.img.get_rect().height:
                return

        if len(self.map_data[self.posx][self.posy]) == 0:
            t1 = 0
        else:
            t1 = max(self.map_data[self.posx][self.posy], key=lambda x: x[1])[1]
        if len(self.map_data[self.posx + a * self.flip][self.posy + b * self.flip]) == 0:
            t2 = 0
        else:
            t2 = max(self.map_data[self.posx + a * self.flip][self.posy + b * self.flip], key=lambda x: x[1])[1]
        if len(self.map_data[self.posx + a * self.flip // 2][self.posy + b * self.flip // 2]) == 0:
            t3 = 0
        else:
            t3 = max(self.map_data[self.posx + a * self.flip // 2][self.posy + b * self.flip // 2], key=lambda x: x[1])[
                1]
        sub = max(abs(t2 - t1), abs(t3 - t1))
        if sub == 0:
            self.posx += a * self.flip
            self.posy += b * self.flip

    def fflip(self):
        self.flip = -self.flip

    def text(self, s, size, x, y):
        font = pygame.font.Font(None, size)
        text = font.render(str(s), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.left = x
        textRect.top = y
        DISPLAYSURF.blit(text, textRect)

    def pos_absolute_center(self, img, x=-1, y=-1, mode=1):
        if x == -1:
            x = center_coordi[0]
        if y == -1:
            y = center_coordi[1]
        if mode == 1:
            DISPLAYSURF.blit(img, (x - img.get_width() / 2, y - img.get_height() / 2))
        else:
            DISPLAYSURF.blit(img, (x, y))

    def minimap(self):
        global idx
        img_map = mlist[idx]
        DISPLAYSURF.blit(img_map, (DISPLAYSURF.get_width() - 310, 10))
        if idx:
            DISPLAYSURF.blit(reddot, (DISPLAYSURF.get_width() - 310 + self.posx - 150, 10 + self.posy - 255))
        else:
            DISPLAYSURF.blit(reddot, (
            DISPLAYSURF.get_width() - 310 + (self.posx - 165) * 300 / 200, 10 + (self.posy - 115) * 300 / 185))

    def detcomplete(self):
        global complete_time, stage_end, stage
        if pygame.time.get_ticks() > complete_time + 0.6 * 5 * 1000:
            self.complete_num = 0
        elif pygame.time.get_ticks() < complete_time + 0.6 * 1000:
            self.complete_num = 1
            stage_end = stage
        elif pygame.time.get_ticks() < complete_time + 0.6 * 2 * 1000:
            self.complete_num = 2
        elif pygame.time.get_ticks() < complete_time + 0.6 * 3 * 1000:
            self.complete_num = 3
        elif pygame.time.get_ticks() < complete_time + 0.6 * 4 * 1000:
            self.complete_num = 4
        elif pygame.time.get_ticks() < complete_time + 0.6 * 5 * 1000:
            self.complete_num = 5


class Door:
    def __init__(self, idx, x1, x2, y1, y2, dest, destx, desty, k, activated=1):
        self.idx = idx
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.dest = dest
        self.destx = destx
        self.desty = desty
        self.k = k
        self.activated = activated

    def move(self, idx, x, y):
        global screen
        if self.activated == -1: return
        if idx == self.idx and self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2:
            screen = screens[self.dest]
            screen.posx = self.destx
            screen.posy = self.desty
            screen.flip = self.k * screens[idx].flip


class Human:
    def __init__(self):
        self.bag = []
        self.grabbing = NoItem
        self.chessImage = pygame.transform.scale(pygame.image.load('./img/chessImage.png').convert_alpha(),
                                                 (909 * 55 / 55.5, 618 * 55 / 55.5))
        self.stx = center_coordi[0] - 864 + 507
        self.sty = center_coordi[1] - 540 + 320

    def showing_bag(self):
        screen.pos_absolute_center(self.chessImage)
        for i, item in enumerate(self.bag):
            l = i % 13
            r = i // 13
            screen.pos_absolute_center(item.image, self.stx + 55 * l + 55 // 2 - item.image.get_width() / 2,
                                       self.sty + 55 * r + 55 // 2 - item.image.get_height() / 2, 0)
        human.get_item()

    def get_item(self):
        flag = 0
        pygame.display.flip()
        while True:
            if flag == 1:
                break
            for event in pygame.event.get():
                if event.type == KEYUP and event.key == K_b:
                    flag = 1
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()

                    if x < self.stx or x > self.stx + 55 * 13 or y < self.sty or y > self.sty + 55 * 8:
                        self.grabbing = NoItem
                        flag = 1
                        break
                    i = (x - self.stx) // 55
                    j = (y - self.sty) // 55
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
        if (x - screen.realx) ** 2 + (y - screen.realy + humanImage.get_height() / 2) ** 2 > 300 ** 2:
            return
        if self.grabbing == NoItem:
            if screen == screens[0]:
                closet.item_activate(x, y)
            erasing = -1
            for i, item in screen.items.items():
                if item.itemrect.left <= x <= item.itemrect.right and item.itemrect.top <= y <= item.itemrect.bottom:
                    erasing = i
                    if type(item) not in self.bag:
                        self.bag.append(type(item))
            if erasing != -1:
                del screen.items[erasing]
        else:
            a, b = screen.coordinate(x, y + self.grabbing.image.get_rect().height / 2)
            new_item = self.grabbing(a, b)
            if not new_item.activate(x, y):
                erasing = -1
                for i, item in screen.items.items():
                    if item.itemrect.left <= x <= item.itemrect.right and item.itemrect.top <= y <= item.itemrect.bottom:
                        erasing = i
                        if (type(item) == CoffeeMix and self.grabbing == WaterBottle) or (type(item) == WaterBottle and
                                                                                          self.grabbing == CoffeeMix):
                            new_item = Coffee(a, b)
                            self.grabbing = NoItem
                            break
                        if (type(item) == Knife and self.grabbing == Fish) or (type(item) == Fish and
                                                                               self.grabbing == Knife):
                            new_item = Graduate(a, b)
                            self.grabbing = NoItem
                            break
                            break
                if erasing != -1:
                    del screen.items[erasing]
                screen.items[(new_item.coorx, new_item.coory)] = new_item
            else:
                self.grabbing = NoItem


class Environment:
    def __init__(self, d=dict()):
        self.dic = d

    def item_activate(self, x, y):
        pass


class ImageEnvironment(Environment):
    def __init__(self, img, a, b, r=0, d=dict()):
        self.img = img
        self.coorx = a
        self.coory = b
        self.r = r
        super().__init__(d)
        self.envrect = pygame.Rect(img.get_rect())

    def item_activate(self, x, y):
        if self.envrect.left <= x <= self.envrect.right and self.envrect.top <= y <= self.envrect.bottom:
            return True
        else:
            return False


class Lake(Environment):
    def __init__(self, d=dict()):
        super().__init__(d)

    def item_activate(self, x, y):
        a, b = screen.coordinate(x, y)
        if len(screen.map_data[a][b]) != 0 and screen.map_data[a][b][0][0] == 103:
            return True
        return False


class WaterOuting(ImageEnvironment):
    image1 = pygame.transform.scale(pygame.image.load("./img/Environments/Water_out2.png"), (150, 150))
    image2 = pygame.transform.scale(pygame.image.load("./img/Environments/Water_out.png"), (150, 150))

    def __init__(self, a, b):
        super().__init__(self.image1, a, b, 3, {"KeyWater": NoItem})

    def item_activate(self, x, y):
        global waterflag
        if self.envrect.left <= x <= self.envrect.right and self.envrect.top <= y <= self.envrect.bottom:
            self.img = self.image2
            waterflag = 0
            fish = Fish(187, 155)
            screens[0].items[(186, 155)] = fish
            return True
        else:
            return False


class Keybox(ImageEnvironment):
    image1 = pygame.transform.scale(pygame.image.load("./img/Environments/key_box.png"), (150, 150))
    image2 = pygame.transform.scale(pygame.image.load("./img/Environments/key_box_water.png"), (150, 150))

    def __init__(self, a, b):
        super().__init__(self.image1, a, b, 3, {"WaterBottle": KeyMaker})

    def item_activate(self, x, y):
        if self.envrect.left <= x <= self.envrect.right and self.envrect.top <= y <= self.envrect.bottom:
            self.img = self.image2
            return True
        else:
            return False


class Closet(ImageEnvironment):
    image = pygame.image.load("./img/Environments/closet.png")
    password = 0

    def __init__(self, a, b, password):
        super().__init__(self.image, a, b, 3)
        self.password = password

    def item_activate(self, x, y):
        if self.envrect.left <= x <= self.envrect.right and self.envrect.top <= y <= self.envrect.bottom:
            input_password(self.password)
            return True
        else:
            return False


class LockMaker(ImageEnvironment):
    def __init__(self, a, b):
        super().__init__(pygame.transform.scale(pygame.image.load("./img/Environments/lock.png"), (220, 332)), a, b, 3,
                         {"KeyMaker": NoItem})

    def item_activate(self, x, y):
        if self.envrect.left <= x <= self.envrect.right and self.envrect.top <= y <= self.envrect.bottom:
            del screen.environments[(self.coorx, self.coory)]
            envs.remove(lock_maker)
            return True
        else:
            return False


class NPC(ImageEnvironment):
    def __init__(self, img, a, b, str, d=dict(), next_str=""):
        super().__init__(img, a, b, 3, d)
        self.str = str
        self.next_str = next_str

    def talk(self):
        screen.text(self.str, 60, center_coordi[0] - 600, center_coordi[1] + 300)

    def item_activate(self, x, y):
        if self.envrect.left <= x <= self.envrect.right and self.envrect.top <= y <= self.envrect.bottom:
            self.str = self.next_str
            return True
        else:
            return False


class Item:
    def __init__(self, a=-1, b=-1, c=-1, d=-1, name=""):
        self.coorx = a
        self.coory = b
        self.standard = (c, d)
        self.name = name

    def activate(self, x, y):
        for env in envs:
            if self.name in env.dic.keys() and env.item_activate(x, y):
                if env.dic[self.name] not in human.bag and env.dic[self.name] != NoItem:
                    human.bag.append(env.dic[self.name])
                return True
        return False


class Graduate(Item):
    image = pygame.image.load('./img/Items/graduate.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height(), "Graduate")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Bottle(Item):
    image = pygame.image.load('./img/Items/bottle.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height(), "Bottle")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Guntlet(Item):
    image = pygame.image.load('./img/Items/guntlet.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height(), "Guntlet")
        self.itemrect = pygame.Rect(self.image.get_rect())


class WaterBottle(Item):
    image = pygame.image.load('./img/Items/waterbottle.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height(), "WaterBottle")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Coffee(Item):
    image = pygame.image.load('./img/Items/coffee.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height(), "Coffee")
        self.itemrect = pygame.Rect(self.image.get_rect())


class CoffeeMix(Item):
    image = pygame.image.load('./img/Items/coffeemix.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height(), "CoffeeMix")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Axe(Item):
    image = pygame.image.load('./img/Items/axe.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Axe")
        self.itemrect = pygame.Rect(self.image.get_rect())


class KeyMaker(Item):
    image = pygame.image.load('./img/Items/key.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "KeyMaker")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Tree(Item):
    image = pygame.image.load('./img/Items/tree.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Tree")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Fish(Item):
    image = pygame.image.load('./img/Items/fish.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Fish")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Knife(Item):
    image = pygame.image.load('./img/Items/knife.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Knife")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Fishing(Item):
    image = pygame.image.load('./img/Items/fishing.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Fishing")
        self.itemrect = pygame.Rect(self.image.get_rect())


class KeyWater(Item):
    image = pygame.image.load('./img/Items/key2.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "KeyWater")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Jewerly1(Item):
    image = pygame.image.load('./img/Items/jewerly1.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Jewerly1")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Jewerly2(Item):
    image = pygame.image.load('./img/Items/jewerly2.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Jewerly2")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Jewerly3(Item):
    image = pygame.image.load('./img/Items/jewerly3.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Jewerly3")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Jewerly4(Item):
    image = pygame.image.load('./img/Items/jewerly4.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Jewerly4")
        self.itemrect = pygame.Rect(self.image.get_rect())


class Jewerly5(Item):
    image = pygame.image.load('./img/Items/jewerly5.png')
    w = image.get_width()
    h = image.get_height()
    if w < h:
        image = pygame.transform.scale(image, (w * 55 // h, 55))
    else:
        image = pygame.transform.scale(image, (55, h * 55 // w))

    def __init__(self, a, b):
        super().__init__(a, b, self.image.get_width() // 2, self.image.get_height() // 2, "Jewerly5")
        self.itemrect = pygame.Rect(self.image.get_rect())


class NoItem(Item):
    image = None


def makedesks(floor, clsnum, a, b):
    global desklist1, desklist2
    if floor == 1:
        desklist = desklist1
    elif floor == 2:
        desklist = desklist2
    else:
        desklist = desklist3
    for i in range(4):
        for j in range(4):
            globals()[f"desk{floor}{clsnum}{i}{j}"] = ImageEnvironment(pygame.image.load('./img/Environments/desk.png'),
                                                                       a + 7 * i, b + 7 * j, 3)
            desklist.append(globals()[f"desk{floor}{clsnum}{i}{j}"])


screens = [Screen('./map/map_data.pkl'), Screen('./map/floor_1.pkl'), Screen('./map/floor_2.pkl'),
           Screen('./map/floor_3.pkl'),
           Screen('./map/floor_4.pkl'), Screen('./map/rooftop.pkl')]
envs = []
doors = [Door(0, 292, 308, 283, 286, 1, 301, 348, 1), Door(0, 288, 294, 245, 245, 1, 275, 251, 1),
         Door(0, 306, 312, 245, 245, 1, 320, 252, 1)
    , Door(1, 271, 329, 249, 250, 0, 300, 243, 1), Door(1, 271, 329, 350, 351, 0, 300, 290, 1)]
for i in range(1, 4):
    doors.append(Door(i, 284, 315, 258, 258, i + 1, 278, 261, -1))
for i in range(2, 5):
    doors.append(Door(i, 271, 283, 257, 258, i - 1, 298, 260, -1))
    doors.append(Door(i, 316, 329, 257, 258, i - 1, 298, 260, -1))
human = Human()
screen = screens[0]
waterflag = 1
desklist1 = []
for clsnum, a, b in [(2, 156, 315), (3, 216, 256), (4, 216, 315), (5, 336, 256), (6, 336, 315), (7, 396, 256),
                     (8, 396, 315)]:
    makedesks(1, clsnum, a + 10, b + 5)
desklist2 = []
for clsnum, a, b in [(1, 156, 256), (2, 156, 315), (3, 216, 256), (4, 216, 315), (5, 276, 315)]:
    makedesks(2, clsnum, a + 10, b + 5)
desklist3 = []
for clsnum, a, b in [(3, 356, 256)]:
    for i in range(10):
        for j in range(10):
            globals()[f"desk{floor}{clsnum}{i}{j}"] = ImageEnvironment(pygame.image.load('./img/Environments/desk.png'),
                                                                       a + 9 * i, b + 9 * j, 3)
            desklist3.append(globals()[f"desk{floor}{clsnum}{i}{j}"])

lock_maker = LockMaker(360, 309)


def input_password(password):
    global complete_time
    psstr = []
    det_inputpassword = 0
    while True:
        global screen
        DISPLAYSURF.blit(inputpassword, (DISPLAYSURF.get_rect().centerx - inputpassword.get_width() / 2, DISPLAYSURF.get_rect().centery - inputpassword.get_height() / 2))
        inputidstr = ''.join(psstr)
        screen.text(inputidstr, 60, DISPLAYSURF.get_width() / 2, DISPLAYSURF.get_height() / 2 - 20)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_RETURN]:
                    if int(''.join(psstr)) == password:
                        complete_time = pygame.time.get_ticks()
                        det_inputpassword = 1
                    else: return
                if keys[K_BACKSPACE]:
                    try:
                        psstr.pop()
                    except:
                        continue
                    continue
                for i in range(len(keys)):
                    if keys[i]: psstr.append(chr(i))

        if det_inputpassword: break

        fpsClock.tick(FPS)
        pygame.display.flip()

    return


def random_generator():
    idx = random.randint(2, 4)
    x, y = -1, -1
    while x == -1 or max(screens[idx].map_data[x][y], key=lambda x: x[1])[1] != 0 or (x, y) in screens[
        idx].environments.keys() \
            or (x, y) in screens[idx].items.keys():
        x = random.randint(151, 449)
        y = random.randint(258, 349)
    return [idx, x, y]


jewerly = []


def game_1():
    bgm_home.stop()
    bgm_stage1.play(-1)
    global envs, gamestarttime, inputidstr, humanImage, stage, closet, showhelp, stage_end, stage
    password = random.randint(1000, 9999)
    closet = Closet(259, 175, password)
    tree1 = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/envtree.png'), (300, 480)),
                             283, 182, 0, {"Axe": Tree})
    tree2 = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/envtree.png'), (300, 480)),
                             311, 179, 0, {"Axe": Tree})
    tree3 = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/envtree.png'), (300, 480)),
                             304, 188, 0, {"Axe": Tree})
    npc = NPC(pygame.transform.scale(pygame.image.load('./img/Environments/stu_6.png'), (100, 225)), 300, 300,
              "Find my 5 gems",
              {"Guntlet": NoItem}, f"Your homebase password is {password}")
    envs = [Lake({"Bottle": WaterBottle, "Fishing": Fish}), tree1, tree2, tree3, npc, closet]
    screens[0].environments = {(283, 182): tree1, (311, 179): tree2, (304, 188): tree3, (259, 175) : closet}
    screens[2].environments = {(300, 300): npc}
    screens[2].npcs = [npc]
    for j in desklist1:
        screens[1].environments[(j.coorx, j.coory)] = j
    for j in desklist3:
        screens[2].environments[(j.coorx, j.coory)] = j
    for i in range(2, 5):
        for j in desklist2:
            screens[i].environments[(j.coorx, j.coory)] = j
    basket = pygame.transform.scale(pygame.image.load('./img/Environments/basket.png').convert_alpha(), (100, 300))
    basketball = pygame.transform.scale(pygame.image.load('./img/Environments/basketball.png').convert_alpha(), (100, 100))
    badminton = pygame.transform.scale(pygame.image.load('./img/Environments/badminton.png').convert_alpha(), (100, 300))
    basket_env = ImageEnvironment(basket, 400, 300, 3)
    basketball_env = ImageEnvironment(basketball, 380, 250, 3)
    badminton_env = ImageEnvironment(badminton, 380, 320, 3)
    envs.extend([badminton_env, basketball_env, basket_env])
    screens[3].environments[(basket_env.coorx, basket_env.coory)] = basket_env
    screens[3].environments[(basketball_env.coorx, basketball_env.coory)] = basketball_env
    screens[3].environments[(badminton_env.coorx, badminton_env.coory)] = badminton_env
    screens[4].environments[(basket_env.coorx, basket_env.coory)] = basket_env
    screens[4].environments[(basketball_env.coorx, basketball_env.coory)] = basketball_env
    screens[4].environments[(badminton_env.coorx, badminton_env.coory)] = badminton_env
    p = random_generator()
    jewerly.append(Jewerly1(p[1], p[2]))
    screens[p[0]].items[(jewerly[0].coorx, jewerly[0].coory)] = jewerly[0]
    p = random_generator()
    jewerly.append(Jewerly2(p[1], p[2]))
    screens[p[0]].items[(jewerly[1].coorx, jewerly[1].coory)] = jewerly[1]
    p = random_generator()
    jewerly.append(Jewerly3(p[1], p[2]))
    screens[p[0]].items[(jewerly[2].coorx, jewerly[2].coory)] = jewerly[2]
    p = random_generator()
    jewerly.append(Jewerly4(p[1], p[2]))
    screens[p[0]].items[(jewerly[3].coorx, jewerly[3].coory)] = jewerly[3]
    p = random_generator()
    jewerly.append(Jewerly5(p[1], p[2]))
    screens[p[0]].items[(jewerly[4].coorx, jewerly[4].coory)] = jewerly[4]
    vx = 0
    vy = 0
    speed = 1
    mode = 0

    gamestarttime = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN or event.type == KEYUP:
                if event.key == K_w:
                    (vx, vy) = (vx, vy - speed) if event.type == KEYDOWN else (0, 0)
                    humanImage = human2
                elif event.key == K_a:
                    (vx, vy) = (vx - speed, vy) if event.type == KEYDOWN else (0, 0)
                    humanImage = human1
                elif event.key == K_s:
                    (vx, vy) = (vx, vy + speed) if event.type == KEYDOWN else (0, 0)
                    humanImage = human1
                elif event.key == K_d:
                    (vx, vy) = (vx + speed, vy) if event.type == KEYDOWN else (0, 0)
                    humanImage = human2

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_f:
                    screen.fflip()
                elif event.key == K_b:
                    human.showing_bag()
                elif event.key == K_h:
                    showhelp *= -1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == 1:
                    screen.click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                else:
                    human.click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        flag = 1
        for i in range(5):
            if type(jewerly[i]) not in human.bag:
                flag = 0
        if flag == 1 and Guntlet not in human.bag:
            human.bag.append(Guntlet)
        screen.move(vx, vy)
        screen.detcomplete()
        if stage_end == 1 and screen.complete_num == 0:
            stage = 2
            break
        screen.makescreen()
        human.grab()
        fpsClock.tick(FPS)
        pygame.display.flip()
    return



def game_2():
    human.bag.clear()
    screens[2].environments.clear()
    screens[2].npcs.clear()
    bgm_stage1.stop()
    bgm_stage2.play(-1)
    global envs, gamestarttime, inputidstr, humanImage, complete_time, screen, showhelp, stage_end, stage
    screen = screens[0]
    screens[0].posx, screens[0].posy = 300, 300

    tree1 = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/envtree.png'), (300, 480)),
                             283, 182, 0, {"Axe": Tree})
    tree2 = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/envtree.png'), (300, 480)),
                             311, 179, 0, {"Axe": Tree})
    tree3 = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/envtree.png'), (300, 480)),
                             304, 188, 0, {"Axe": Tree})
    npc_water = NPC(pygame.transform.scale(pygame.image.load('./img/Environments/stu_1.png'), (102, 222)), 284, 276,
                    "I want some water...", {"WaterBottle": CoffeeMix}, "Thank you!")
    npc_coffee = NPC(pygame.transform.scale(pygame.image.load('./img/Environments/teacher_1.png'), (102, 222)), 330, 300
                     , "Can you give me coffee?", {"Coffee": KeyWater}, "You can remove water by this!")
    keybox = Keybox(325, 311)
    printer = ImageEnvironment(pygame.transform.scale(pygame.image.load('./img/Environments/printer.png'), (200, 200)),
                               380, 328, 3, {"Tree": Fishing})

    waterouting = WaterOuting(257, 156)

    envs = [Lake({"Bottle": WaterBottle, "Fishing": Fish}), tree1, tree2, tree3, npc_water, keybox, printer,
            lock_maker, npc_coffee, waterouting]
    screens[0].environments = {(283, 182): tree1, (311, 179): tree2, (304, 188): tree3,
                               (257, 156): waterouting}
    screens[3].environments = {(330, 300): npc_coffee}
    screens[1].environments = {(380, 328): printer, (360, 309): lock_maker, (284, 276): npc_water, (325, 311): keybox}
    screens[3].npcs = [npc_coffee]
    screens[1].npcs = [npc_water]
    for j in desklist1:
        screens[1].environments[(j.coorx, j.coory)] = j
    for j in desklist3:
        screens[2].environments[(j.coorx, j.coory)] = j
    for i in range(2, 5):
        for j in desklist2:
            screens[i].environments[(j.coorx, j.coory)] = j
    basket = pygame.transform.scale(pygame.image.load('./img/Environments/basket.png').convert_alpha(), (100, 300))
    basketball = pygame.transform.scale(pygame.image.load('./img/Environments/basketball.png').convert_alpha(), (100, 100))
    badminton = pygame.transform.scale(pygame.image.load('./img/Environments/badminton.png').convert_alpha(), (100, 300))
    basket_env = ImageEnvironment(basket, 400, 300, 3)
    basketball_env = ImageEnvironment(basketball, 400, 400, 3)
    badminton_env = ImageEnvironment(badminton, 400, 350, 3)
    envs.extend([badminton_env, basketball_env, basket_env])
    screens[3].environments[(basket_env.coorx, basket_env.coory)] = basket_env
    screens[3].environments[(basketball_env.coorx, basketball_env.coory)] = basketball_env
    screens[3].environments[(badminton_env.coorx, badminton_env.coory)] = badminton_env
    screens[4].environments[(basket_env.coorx, basket_env.coory)] = basket_env
    screens[4].environments[(basketball_env.coorx, basketball_env.coory)] = basketball_env
    screens[4].environments[(badminton_env.coorx, badminton_env.coory)] = badminton_env
    p = random_generator()
    bottle = Bottle(p[1], p[2])

    screens[p[0]].items[(bottle.coorx, bottle.coory)] = bottle
    p = random_generator()
    axe = Axe(p[1], p[2])

    screens[p[0]].items[(axe.coorx, axe.coory)] = axe
    p = random_generator()
    knife = Knife(p[1], p[2])

    screens[p[0]].items[(knife.coorx, knife.coory)] = knife
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
                    (vx, vy) = (vx, vy - speed) if event.type == KEYDOWN else (0, 0)
                    humanImage = human2
                elif event.key == K_a:
                    (vx, vy) = (vx - speed, vy) if event.type == KEYDOWN else (0, 0)
                    humanImage = human1
                elif event.key == K_s:
                    (vx, vy) = (vx, vy + speed) if event.type == KEYDOWN else (0, 0)
                    humanImage = human1
                elif event.key == K_d:
                    (vx, vy) = (vx + speed, vy) if event.type == KEYDOWN else (0, 0)
                    humanImage = human2

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_f:
                    screen.fflip()
                elif event.key == K_b:
                    human.showing_bag()
                elif event.key == K_h:
                    showhelp *= -1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mode == 1:
                    screen.click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                else:
                    human.click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

        screen.move(vx, vy)
        screen.detcomplete()
        if stage_end == 2  and screen.complete_num == 0: break
        screen.makescreen()
        human.grab()
        if Graduate in human.bag:
            complete_time = pygame.time.get_ticks()
            human.bag.remove(Graduate)
        fpsClock.tick(FPS)
        pygame.display.flip()
    return



def inputid():  # inputid 가 최종 입력된 사용자 id
    global inputidstr
    sli = []
    det_inputid = 0
    while True:
        global screen
        DISPLAYSURF.blit(inputidimg, (0, 0))
        inputidstr = ''.join(sli)
        screen.text(inputidstr, 60, DISPLAYSURF.get_width() / 3, DISPLAYSURF.get_height() / 2 - 20)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_RETURN]:
                    det_inputid = 1
                if keys[K_BACKSPACE]:
                    try:
                        sli.pop()
                    except:
                        continue
                    continue
                for i in range(len(keys)):
                    if keys[i]: sli.append(chr(i))

        if det_inputid: break

        fpsClock.tick(FPS)
        pygame.display.flip()

    return


def startgame():
    bgm_home.play(-1)
    global idtime, gamestarttime, endtime
    tuto = -1
    while True:
        DISPLAYSURF.blit(start_img, (0, 0))
        DISPLAYSURF.blit(tutorial_img, ((DISPLAYSURF.get_rect().centerx + DISPLAYSURF.get_width()) / 2,
                                        (DISPLAYSURF.get_rect().centery - DISPLAYSURF.get_height() / 4)))
        DISPLAYSURF.blit(play_img, ((DISPLAYSURF.get_rect().centerx + DISPLAYSURF.get_width()) / 2,
                                    (DISPLAYSURF.get_rect().centery + DISPLAYSURF.get_height() / 4)))
        rect_tutorial.left = (DISPLAYSURF.get_rect().centerx + DISPLAYSURF.get_width()) / 2
        rect_tutorial.top = (DISPLAYSURF.get_rect().centery - DISPLAYSURF.get_height() / 4)
        rect_play.left = (DISPLAYSURF.get_rect().centerx + DISPLAYSURF.get_width()) / 2
        rect_play.top = DISPLAYSURF.get_rect().centery + DISPLAYSURF.get_height() / 4
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                startx1, starty1 = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                if (rect_tutorial[0] <= startx1 <= rect_tutorial[0] + rect_tutorial[2]) and (
                        rect_tutorial[1] <= starty1 <= rect_tutorial[1] + rect_tutorial[3]):
                    tuto *= -1
                if (rect_play[0] <= startx1 <= rect_play[0] + rect_play[2]) and (
                        rect_play[1] <= starty1 <= rect_play[1] + rect_play[3]):
                    with open('./idtime.pkl', 'rb') as f:
                        idtime = pickle.load(f)
                    inputid()
                    game_1()
                    game_2()
                    endtime = (pygame.time.get_ticks() - gamestarttime) // 1000
                    idtime.append((inputidstr, endtime))
                    with open('./idtime.pkl', 'wb') as f:
                        pickle.dump(idtime, f, protocol=pickle.HIGHEST_PROTOCOL)
                    ending()
        if tuto == 1: DISPLAYSURF.blit(tuto_img, (DISPLAYSURF.get_rect().centerx - DISPLAYSURF.get_height() / 2, 0))

        pygame.display.flip()


def ending():
    bgm_stage2.stop()
    global idtime, endtime
    while True:
        DISPLAYSURF.blit(end_img, (0, 0))
        idtime.sort(key=lambda x: x[1])
        dett = 0

        for i in range(min(10, len(idtime))):
            id, time = idtime[i]
            if (id, time) == (inputidstr, endtime):
                dett = 1
                ii = i
            screen.text(f'{i + 1} [{id}] {time}s', 30, DISPLAYSURF.get_rect().centerx - 340,
                        DISPLAYSURF.get_rect().centery - 200 + 40 * i)
            try:
                DISPLAYSURF.blit(you,
                                 (DISPLAYSURF.get_rect().centerx - 400, DISPLAYSURF.get_rect().centery - 210 + 40 * ii))
            except:
                pass

        if not dett:
            i = idtime.index((inputidstr, endtime))
            screen.text(f'{i + 1} [{inputidstr}] {endtime}s', 30, DISPLAYSURF.get_rect().centerx - 340,
                        DISPLAYSURF.get_rect().centery - 200 + 40 * 10)
            DISPLAYSURF.blit(you,
                             (DISPLAYSURF.get_rect().centerx - 400, DISPLAYSURF.get_rect().centery - 210 + 40 * 10))

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        pygame.display.flip()


startgame()