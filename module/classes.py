import pygame, random

global basic_bee_img
# global basic_hornet_img
global flowers


def init_bee(bb_img):
    global basic_bee_img
    basic_bee_img = bb_img
# def init_hornet(bh_img):
#     basic_hornet_img = bh_img
def init_flower(flowertypes: list):
    flowers = flowertypes


class basic_bee:
    cost = 100
    def __init__(self):
        self.hp = 10
        self.collect_rate = 1
        self.name = "Basic Bee"
        self.image = basic_bee_img
        self.speed = random.randint(5, 13) / 10
# --- Define the hornets as classes ---
class basic_hornet:
    def __init__(self):
        self.hp = 25
        self.atk = 2
        self.name = "Basic Hornet"

# --- Define the general "bee" class ---
class Bee:
    def __init__(self, width_height: list, type):
        self.type = type
        self.hp = type.hp
        self.collect_rate = type.collect_rate
        self.name = type.name
        self.clk = False
        self.image = type.image
        self.rect = self.image.get_rect()
        self.speed = type.speed
        self.pos = [0, 0]
        self.aim_pos = [random.randint(75, width_height[0] - 75), random.randint(75, width_height[1] - 75)]

# Buttons
class button:
    def __init__(self, width_height: list, xypos: list):
        self.xpos = xypos[0]
        self.ypos = xypos[1]
        self.width = width_height[0]
        self.height = width_height[1]
    def show(self, surface, color: list=(0, 0, 0)):
        pygame.draw.rect(surface, color, (self.xpos, self.ypos, self.width, self.height))
    def onHover(self, mouse_pos: list):
        return (mouse_pos[0] >= self.xpos and mouse_pos[0] <= (self.xpos + self.width)) and (mouse_pos[1] >= self.ypos and mouse_pos[1] <= (self.ypos + self.height))

class flower:
    cost = 250
    def __init__(self, wh, image):
        self.image = pygame.transform.scale(image, (50, 50))
        self.pos = [random.randint(50, wh[0] - 75), random.randint(50, wh[1] - 130)]
        self.hp = 120

    def show(self, surface):
        surface.blit(self.image, self.pos)