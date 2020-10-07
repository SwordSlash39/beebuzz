# ----- IMPORTS -----
# --- Classic ---
import pygame, json, random, math

# --- Self Files ---
import module.special_quit, module.keyboard
from module import classes as cls
with open('title.json') as f:
    title = json.load(f)
# -------------------

# ----- DEFINITIONS -----
# New Text
def new_text(txt: str, font: str, fontsize: float):
    return pygame.font.SysFont(font, fontsize).render(txt, False, (0, 0, 0))

# Bee draws
def draw_bees():
    if not inShop and not inCode:
        for e in range(len(bees)):
            least_index = 0
            least = math.sqrt(math.pow(bees[least_index].pos[0] - flowers[least_index].pos[0], 2) + math.pow(bees[least_index].pos[1] - flowers[least_index].pos[1], 2))
            for i in range(len(flowers)):
                # Find dist
                txt = math.sqrt(math.pow(bees[e].pos[0] - flowers[i].pos[0], 2) + math.pow(bees[e].pos[1] - flowers[i].pos[1], 2))
                if txt < 0:
                    txt *= -1
                if txt < least:
                    least = txt
                    least_index = i
            bees[e].aim_pos = flowers[least_index].pos
            if math.sqrt(math.pow(bees[e].pos[0] - flowers[least_index].pos[0], 2) + math.pow(bees[0].pos[1] - flowers[least_index].pos[1], 2)) <= 50:
                for search in flowers:
                    if search.pos == bees[e].aim_pos:
                        search.hp -= 1
                        if search.hp <= 0:
                            # Award + Revive
                            global money
                            money += 10
                            search.pos = [random.randint(wh[0] // 2, wh[0] - 75), random.randint(50, wh[1] - 75)]
                            search.hp = 120
                            bees[e].aim_pos = (0, 0)
            else:
                # X coord change
                if bees[e].pos[0] > bees[e].aim_pos[0]:
                    bees[e].pos[0] -= bees[e].speed
                elif bees[e].pos[0] < bees[e].aim_pos[0]:
                    bees[e].pos[0] += bees[e].speed
                # Y coord change
                if bees[e].pos[1] > bees[e].aim_pos[1]:
                    bees[e].pos[1] -= bees[e].speed
                elif bees[e].pos[1] < bees[e].aim_pos[1]:
                    bees[e].pos[1] += bees[e].speed               
            screen.blit(bees[e].image, bees[e].pos)

# Txt showing
def show_txts():
    if muted:   # Play/Pause text for music
        mute_music_msg = new_text("X", "Comic Sans MS", 30)
    else:
        mute_music_msg = new_text("O", "Comic Sans MS", 30)
    screen.blit(mute_music_msg, (wh[0] - 50, 0))
    if inCode:
        screen.blit(redeem_txt, (550, 350))
        input_txt = new_text(enter, "Comic Sans MS", 30)
        screen.blit(input_txt, (200, 175))
    else:
        txt = "c{}".format(money)
        coins_msg = new_text(txt, "Comic Sans MS", 30)   # Money text
        txt = len(txt) * 10
        screen.blit(coins_msg, (wh[0] // 2 - txt, wh[1] - 50))
        if inShop:
            shop_home = new_text("Home", "Comic Sans MS", 30)   # "Home" Screen at shop
            screen.blit(shop_home, (wh[0] - 100, wh[1] - 50))
            screen.blit(in_shop_msg, (500, 0))  # "<project_name>" Shop (in shop menu)
            """The Shop texts"""
            screen.blit(cost_basic_bee_amt, (70, 100))
            screen.blit(cost_basic_bee, (70, 70))
            screen.blit(cost_new_flower_amt, (70, 620))
            screen.blit(cost_new_flower, (70, 590))
        else:        
            screen.blit(history_txt, (0, wh[1] - 40))   # "Save Data" Text
            screen.blit(name_of_project, (500, 0))   # Buzz logo (name of proj.)
            screen.blit(owner, (550, 40))  # Made by <person>
            shop_home = new_text("Shop", "Comic Sans MS", 30)   # "Shop" print at main menu
            screen.blit(shop_home, (wh[0] - 100, wh[1] - 50))

# Button showing
def draw_buttons(mouse_pos: list):
    if mute_music_btn.onHover(mouse_pos):   # Mute/Unmute music Button
        mute_music_btn.show(screen, (255, 150, 0))
    else:
        mute_music_btn.show(screen, (255, 200, 50))
    
    if shop_btn.onHover(mouse_pos):   # Shop Button
        shop_btn.show(screen, (200, 50, 50))
    else:
        shop_btn.show(screen, (255, 0, 0))
    
    if inCode:
        if redeem_btn.onHover(mouse_pos):
            redeem_btn.show(screen, (0, 100, 200))
        else:
            redeem_btn.show(screen, (100, 100, 200))
    else:
        if inShop:
            for i in range(len(rect_inshops)):
                if rect_inshops[i].onHover(mouse_pos):
                    rect_inshops[i].show(screen, (255, 200, 100))
                else:
                    rect_inshops[i].show(screen, YELLOW)
        else:
            if history.onHover(mouse_pos):   # Save Button
                history.show(screen, (0, 100, 255))
            else:
                history.show(screen, (100, 100, 255))

# Showing Flowers
def draw_flower():
    if not inShop and not inCode:
        for i in range(len(flowers)):
            flowers[i].show(screen)

# Background maintenance
def background_draw():
    if inShop:
        screen.fill(GREEN)
        return None
    if inCode:
        screen.fill(RED)
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((200, 100), (850, 200)))
        return None
    screen.fill(WHITE)
# -----------------------

# ----- SET-UP -----
global bees, money
bees = []
flowers = []
money = 0
# Storing of vars
txt = ""
# Codes
allCodes = ["beebee"]
txt = open("data/codes.txt", "r")
codesRedeemed = []
txt.close()
# In somewhere
inCode = False
inShop = False
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# To bee added
"""try:
    codesRedeemed = eval(txt.read())
except:
    codesRedeemed = []"""
# ------------------

# ----- INITIALISE -----
global screen
# Init (pygame)
pygame.init()
pygame.font.init()
pygame.mixer.init()
# Set up screen
wh = (1250, 800)
screen = pygame.display.set_mode(wh)
pygame.display.set_caption("BUG WORLD")
# Pygame Icon
programIcon = pygame.image.load(title["logo"])
pygame.display.set_icon(programIcon)
# Background
screen.fill(WHITE)
# Clock
clock = pygame.time.Clock()
# Music (for Background)
pygame.mixer.music.load("music/background/background_music.wav")
muted = False
# Pygame Images
    # Bees
basic_bee_img = pygame.image.load("images/bees/basic_bee.png").convert()
basic_bee_img = pygame.transform.scale(basic_bee_img, (60, 50))
    # Flowers
green_flower = pygame.image.load("images/flower/green_flower.png").convert()
for i in range(3):
    flowers.append(cls.flower(wh, green_flower))
# Pygame Fonts/Texts
name_of_project = new_text(title["name"], "Comic Sans MS", 30)
owner = new_text("By {}".format(title["credits"]["owner"]), "Comic Sans MS", 14)
in_shop_msg = new_text("{} shop".format(title["name"]), "Comic Sans MS", 30)
history_txt = new_text("Download History", "Comic Sans MS", 20)
if muted:
    mute_music_msg = new_text("X", "Comic Sans MS", 30)
else:
    mute_music_msg = new_text("O", "Comic Sans MS", 30)
"""Shop Texts"""
shop_home = new_text("Shop", "Comic Sans MS", 30)
coins_msg = new_text("c{}".format(money), "Comic Sans MS", 30)
# Pygame Buttons
shop_btn = cls.button((100, 50), (wh[0] - 100, wh[1] - 50))
history = cls.button((170, 50), (0, wh[1] - 50))
mute_music_btn = cls.button((75, 75), (wh[0] - 50, 0)) # O - playing; X - stopped
# SHOP
"""Shop surfaces"""
rect_inshops = []
basic_bee_buy = cls.button((200, 200), (50, 50))
rect_inshops.append(basic_bee_buy)
rect_top_center = cls.button((200, 200), (wh[0] // 2 - 135, 50))
rect_inshops.append(rect_top_center)
rect_top_right = cls.button((200, 200), (wh[0] - 250, 50))
rect_inshops.append(rect_top_right)

rect_center_left = cls.button((200, 200), (50, 300))
rect_inshops.append(rect_center_left)
rect_center_center = cls.button((200, 200), (wh[0] // 2 - 135, 300))
rect_inshops.append(rect_center_center)
rect_center_right = cls.button((200, 200), (wh[0] - 250, 300))
rect_inshops.append(rect_center_right)

flower_buy = cls.button((200, 200), (50, 550))
rect_inshops.append(flower_buy)
rect_down_center = cls.button((200, 200), (wh[0] // 2 - 135, 550))
rect_inshops.append(rect_down_center)
rect_down_right = cls.button((200, 200), (wh[0] - 250, 550))
rect_inshops.append(rect_down_right)
"""Shop texts"""
cost_basic_bee = new_text("Basic Bee", "Comic Sans MS", 30)
cost_basic_bee_amt = new_text("c{}".format(cls.basic_bee.cost), "Comic Sans MS", 30)
cost_new_flower = new_text("+Flower", "Comic Sans MS", 30)
cost_new_flower_amt = new_text("c{}".format(cls.flower.cost), "Comic Sans MS", 30)
# CODE REDEEM
"""Buttons"""
redeem_btn = cls.button((200, 75), (525, 350))
"""Texts"""
redeem_txt = new_text("Redeem!", "Comic Sans MS", 30)
enter = ""
input_txt = new_text(enter, "Comic Sans MS", 30)


# Init (Custom modules)
cls.init_bee(bb_img=basic_bee_img)
cls.init_flower(flowers)
# ----------------------

# ----- MAIN LOOP -----
bees.append(cls.Bee(wh, cls.basic_bee()))
bees[0].aim_pos = random.choice(flowers).pos
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)
while True:
    try:
        background_draw()
        mouse = pygame.mouse.get_pos()
        txt = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_btn.onHover(mouse):
                    inShop = not inShop
                if inShop:
                    if basic_bee_buy.onHover(mouse):
                        if money >= 100:
                            bees.append(cls.Bee(wh, cls.basic_bee()))
                            bees[len(bees) - 1].aim_pos = random.choice(flowers).pos
                            money -= 100
                    if flower_buy.onHover(mouse):
                        if money >= 250:
                            flowers.append(cls.flower(wh, green_flower))
                            money -= 250
                if mute_music_btn.onHover(mouse):
                    muted = not muted
                    if muted:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                if inCode:
                    if redeem_btn.onHover(mouse):
                        if enter in allCodes:
                            if enter in codesRedeemed:
                                enter = "Already redeemed code!"
                            else:
                                txt1 = [random.randint(0, 2), enter]
                                if txt1[0] == 0:
                                    for i in range(3):
                                        bees.append(cls.Bee(wh, cls.basic_bee()))
                                    enter = "Congrats! You got 3 basic bees!"
                                elif txt1[0] == 1:
                                    for i in range(3):
                                        flowers.append(cls.flower(wh, green_flower))
                                    enter = "Congrats! You got 3 flowers!"
                                elif txt1[0] == 3:
                                    money += 1000
                                    enter = "Congrats! You got c1000!"
                                codesRedeemed.append(txt1[1])
                                editCodes = open("data/codes.txt", "w")
                                editCodes.write(str(codesRedeemed))
                                editCodes.close()
                        else:
                            enter = "Error! Wrong Code!"
            if event.type == pygame.KEYDOWN:
                if inCode and txt:
                    if module.keyboard.keyboard_check(event.key) is None:
                        pass
                    else:
                        txt = False
                        enter += module.keyboard.keyboard_check(event.key)
                if event.key == pygame.K_RSHIFT:
                    if not inShop:
                        inCode = not inCode
                        if inCode:
                            enter = ""
                            input_txt = new_text(enter, "Comic Sans MS", 30)

        # All actions must draw
        draw_buttons(mouse)
        show_txts()
        # Only specific actions
        draw_flower()
        draw_bees()

        # --- Update Screen ---
        pygame.display.update()
        clock.tick(60)
    except pygame.error:
        break
# ---------------------
module.special_quit.quit("Exited the game with runtime {} seconds successfully!")