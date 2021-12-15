import pygame, math, random
from pygame import mixer
pygame.init()
mixer.init()
from sys import exit

swipe = pygame.mixer.Sound("Sounds/swipe.mp3")

class Background(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/bg.png"), (1920, 1080))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        pass


class Card(pygame.sprite.Sprite):
    def __init__(self, pos, value, suit, isFlipped):
        pygame.sprite.Sprite.__init__(self)
        self.card_size = (80, 115)
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", int(self.card_size[1]/2))
        self.value = value
        self.isFlipped = isFlipped
        if suit in ["clover", "spade"]:
            self.colour = (0, 0, 0)
        else:
            self.colour = (200, 0, 0)
        if self.isFlipped:
            self.image = pygame.transform.scale(pygame.image.load("Misc/back.png"), self.card_size)
            self.stored = pygame.transform.scale(pygame.image.load("Misc/" + suit + ".png"), self.card_size)
            self.textSurf = self.font.render("", False, self.colour)
        else:
            self.image = pygame.transform.scale(pygame.image.load("Misc/" + suit + ".png"), self.card_size)
            self.textSurf = self.font.render(self.value, False, self.colour)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.textrect = self.textSurf.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.textSurf, self.textrect)

    def update(self):
        self.textrect = self.textSurf.get_rect(center=self.image.get_rect().center)
        self.image.blit(self.textSurf, self.textrect)
        pass


class TextBox(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/txtbox.png"), (600, 150))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 24)
        self.current_letter = 0
        self.text = ""
        self.isWriting = False
        textSurf = self.font.render(self.text, False, (56, 82, 49))
        textrect = textSurf.get_rect(center=self.image.get_rect().center)
        self.image.blit(textSurf, textrect)
        self.tocks = [pygame.mixer.Sound("Sounds/tock1.wav"), pygame.mixer.Sound("Sounds/tock2.wav"),
                 pygame.mixer.Sound("Sounds/tock3.wav")]

    def update(self):
        pass

    def clear(self):
        self.image = pygame.transform.scale(pygame.image.load("Misc/txtbox.png"), (600, 150))

    def write(self, str, uif):
        self.text = ""
        self.clear()
        talk = True
        while talk:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.text = str
                    self.clear()
                    textSurf = self.font.render(self.text, False, (56, 82, 49))
                    textrect = textSurf.get_rect(center=self.image.get_rect().center)
                    self.image.blit(textSurf, textrect)
                    self.isWriting = False
                    uif[0].isTalking = False
                    talk = False

            if talk == False:
                break

            if self.current_letter < len(str):
                uif[0].isTalking = True
                self.isWriting = True

                if self.current_letter % 1 == 0:
                    self.text += str[int(self.current_letter)]
                    pygame.mixer.Sound.play(self.tocks[random.randint(0, 2)])
                self.current_letter += 0.5
                self.clear()
                textSurf = self.font.render(self.text, False, (56, 82, 49))
                textrect = textSurf.get_rect(center=self.image.get_rect().center)
                self.image.blit(textSurf, textrect)
            else:
                if self.isWriting:
                    last = pygame.time.get_ticks()
                    self.isWriting = False
                    uif[0].isTalking = False
                if pygame.time.get_ticks() - last >= 500:
                    break
            uif[1].update()
            uif[1].draw(uif[2])
            pygame.display.flip()

        self.current_letter = 0


class Connor(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.isTalking = False
        self.sprites_idle = []
        self.sprites_talk = []
        for i in range(0, 2):
            self.sprites_idle.append(pygame.image.load("Connor_Idle/idle_" + str(i) + ".png"))
        for i in range(0, 6):
            self.sprites_talk.append(pygame.image.load("Connor_Talk/talk_" + str(i) + ".png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites_idle[self.current_sprite], (512, 736))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if not self.isTalking:
            self.current_sprite += 0.02
            if int(self.current_sprite) >= len(self.sprites_idle):
                self.current_sprite = 0
            self.image = pygame.transform.scale(self.sprites_idle[int(self.current_sprite)], (512, 736))
        else:
            self.current_sprite += 0.5
            if int(self.current_sprite) >= len(self.sprites_talk):
                self.current_sprite = 0
            self.image = pygame.transform.scale(self.sprites_talk[int(self.current_sprite)], (512, 736))


class CPU(pygame.sprite.Sprite):
    def __init__(self, pos, id):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.sprites_idle = []
        self.busted = False
        if id == 1:
            self.j = 9
        elif id == 2:
            self.j = 28
        else:
            self.j = 36
        for i in range(0, self.j):
            self.sprites_idle.append(
                pygame.image.load("CPU" + str(id) + "_Idle/Cpu" + str(id) + "_Idle" + str(i) + ".png"))
        self.current_sprite = 0
        self.image = pygame.transform.scale(self.sprites_idle[self.current_sprite], (192, 276))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if self.busted:
            self.image = pygame.transform.scale(self.sprites_idle[self.j-1], (192, 276))
            return

        if self.id == 2:
            self.current_sprite += 0.25
            if int(self.current_sprite) >= len(self.sprites_idle)-1:
                self.current_sprite = 0
            self.image = pygame.transform.scale(self.sprites_idle[int(self.current_sprite)], (192, 276))
        else:
            self.current_sprite += 0.1
            if int(self.current_sprite) >= len(self.sprites_idle)-1:
                self.current_sprite = 0
            self.image = pygame.transform.scale(self.sprites_idle[int(self.current_sprite)], (192, 276))

    def bust(self):
        self.busted = True


class Board(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/talble.png"), (1050, 700))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 40)
        self.font2 = pygame.font.Font("Misc/PIXELADE.TTF", 40)
        self.font.underline = True

    def update(self):
        pass

    def board_update(self, ct, pt):
        ct_title = self.font.render("Call Target", False, (255, 255, 255))
        pot_title = self.font.render("Pot", False, (255, 255, 255))
        call_target = self.font2.render("$"+str(ct), False, (255, 255, 255))
        pot_value = self.font2.render("$"+str(pt), False, (255, 255, 255))
        board_surf = [ct_title, pot_title, call_target, pot_value]

        ctt_rect = ct_title.get_rect(center=(self.image.get_rect().centerx-150, self.image.get_rect().centery-50))
        pt_rect = pot_title.get_rect(center=(self.image.get_rect().centerx+150, self.image.get_rect().centery-50))
        ctv_rect = call_target.get_rect(center=(self.image.get_rect().centerx-150, self.image.get_rect().centery))
        pot_rect = pot_value.get_rect(center=(self.image.get_rect().centerx+150, self.image.get_rect().centery))
        board_rect = [ctt_rect, pt_rect, ctv_rect, pot_rect]

        self.image = pygame.transform.scale(pygame.image.load("Misc/talble.png"), (1050, 700))

        for i in range(0, len(board_rect)):
            self.image.blit(board_surf[i], board_rect[i])

class Stack(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/stack.png"), (82, 117))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        pass


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, text):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/Button.png"), (300, 100))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 66)
        textSurf = self.font.render(text, False, (5, 36, 0))
        textrect = textSurf.get_rect(center=self.image.get_rect().center)
        self.image.blit(textSurf, textrect)

    def update(self):
        pass


class Frame(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/frame.png"), (280, 200))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 30)
        textSurf = self.font.render("Your cards", False, (255, 255, 255))
        textrect = textSurf.get_rect(center= (self.image.get_rect().centerx, self.image.get_rect().centery-80))
        self.image.blit(textSurf, textrect)

    def update(self):
        pass


class Knob(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/knob.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.prop = 0.5
        self.pos = pos
        self.rect.center = (pos[0], pos[1]+27)

    def update(self):
        mouse = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.rect.centerx - 35 < mouse[0] < self.rect.centerx + 35 and self.rect.centery - 35 < mouse[1] < self.rect.centery + 35:
            self.rect.centerx = mouse[0]
            if self.rect.centerx >= self.pos[0] + 300:
                self.rect.centerx = self.pos[0] + 300
            elif self.rect.centerx <= self.pos[0] - 300:
                self.rect.centerx = self.pos[0] - 300

            self.prop = (self.rect.centerx + 300 - self.pos[0]) / 600


class Slider(pygame.sprite.Sprite):
    def __init__(self, pos, prop, pm):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/bar.png"), (600, 100))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.value = round(prop * pm)
        if 0 < self.value < pm:
            text = str(self.value)
        elif self.value == 0:
            self.value = 1
            text = str(self.value)
        else:
            text = "ALL-IN"
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 40)
        textSurf = self.font.render(text, False, (5, 36, 0))
        textrect = textSurf.get_rect(center=(self.image.get_rect().centerx, self.image.get_rect().centery-17))
        self.image.blit(textSurf, textrect)

    def update(self):
        pass

    def value_update(self, prop, pm):
        self.value = round(prop * pm)
        if 0 < self.value < pm:
            text = str(self.value)
        elif self.value == 0:
            self.value = 1
            text = str(self.value)
        else:
            text = "ALL-IN"
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 40)
        textSurf = self.font.render(text, False, (5, 36, 0))
        textrect = textSurf.get_rect(center=(self.image.get_rect().centerx, self.image.get_rect().centery-17))
        self.image = pygame.transform.scale(pygame.image.load("Misc/bar.png"), (600, 100))
        self.image.blit(textSurf, textrect)


class Blind(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "big":
            self.image = pygame.transform.scale(pygame.image.load("Misc/bigblind.png"), (100, 100))
        else:
            self.image = pygame.transform.scale(pygame.image.load("Misc/smallblind.png"), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        pass

class Status(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Misc/Button.png"), (650, 275))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.font = pygame.font.Font("Misc/PIXELADE.TTF", 40)
        self.font2 = pygame.font.Font("Misc/PIXELADE.TTF", 50)
        self.font3 = pygame.font.Font("Misc/PIXELADE.TTF", 50)
        self.font2.underline = True


    def update(self):
        pass

    def text_update(self, pm , c1m, c2m , c3m, round):
        money_title = self.font2.render("Balance", False, (5, 36, 0))
        round_title = self.font2.render("Round", False, (5, 36, 0))
        money1 = self.font.render("Player: " + str(pm), False, (5, 36, 0))
        money2 = self.font.render("CPU1: " + str(c1m), False, (5, 36, 0))
        money3 = self.font.render("CPU2: " + str(c2m), False, (5, 36, 0))
        money4 = self.font.render("CPU3: " + str(c3m), False, (5, 36, 0))
        round_counter = self.font3.render(str(round), False, (5, 36, 0))
        stat_surf = [money1, money2, money3, money4, money_title, round_title, round_counter]

        money1_s = money1.get_rect(center=(self.image.get_rect().centerx + 110, self.image.get_rect().centery - 30))
        money2_s = money2.get_rect(center=(self.image.get_rect().centerx + 110, self.image.get_rect().centery))
        money3_s = money3.get_rect(center=(self.image.get_rect().centerx + 110, self.image.get_rect().centery + 30))
        money4_s = money4.get_rect(center=(self.image.get_rect().centerx + 110, self.image.get_rect().centery + 60))
        mtitle_s = money_title.get_rect(
            center=(self.image.get_rect().centerx + 110, self.image.get_rect().centery - 70))
        rtitle_s = round_title.get_rect(
            center=(self.image.get_rect().centerx - 110, self.image.get_rect().centery - 25))
        counter_s = round_counter.get_rect(
            center=(self.image.get_rect().centerx - 110, self.image.get_rect().centery + 20))
        stat_rect = [money1_s, money2_s, money3_s, money4_s, mtitle_s, rtitle_s, counter_s]

        self.image = pygame.transform.scale(pygame.image.load("Misc/Button.png"), (650, 275))
        for i in range(0, len(stat_surf)):
            self.image.blit(stat_surf[i], stat_rect[i])


def move_card(card, dest, speed, uif):
    dx = dest[0] - card.rect.centerx
    dy = dest[1] - card.rect.centery
    tx = 0
    ty = 0
    if dx == 0:
        theta = math.copysign(math.pi/2, dy)
    else:
        theta = math.atan(abs(dy / dx))

    pygame.mixer.Sound.play(swipe)
    while abs(tx) < abs(dx) or abs(ty) < abs(dy):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        if abs(tx) < abs(dx):
            if dx < 0:
                card.rect.centerx -= speed * math.cos(theta)
                tx -= speed * math.cos(theta)
            else:
                card.rect.centerx += speed * math.cos(theta)
                tx += speed * math.cos(theta)
        if abs(ty) < abs(dy):
            if dy < 0:
                card.rect.centery -= speed * math.sin(theta)
                ty -= speed * math.sin(theta)
            else:
                card.rect.centery += speed * math.sin(theta)
                ty += speed * math.sin(theta)

        uif[1].update()
        uif[1].draw(uif[2])
        pygame.display.flip()

    card.rect.centerx = dest[0]
    card.rect.centery = dest[1]


def flip_card(card, uif):
    width = card.card_size[0]
    flipped = False

    pygame.mixer.Sound.play(swipe)
    while True:
        if not flipped:
            width -= 10
            card.image = pygame.transform.scale(card.image, (width, card.card_size[1]))
        else:
            width += 10
            card.image = pygame.transform.scale(card.stored, (width, card.card_size[1]))

        if width <= 0:
            flipped = True
            card.isFlipped = False
            card.textSurf = card.font.render(card.value, False, card.colour)
        elif width >= card.card_size[0] and flipped:
            break

        uif[1].update()
        uif[1].draw(uif[2])
        pygame.display.flip()


def sin_card(cards, val, offset):
    for i in range(0, len(cards)):
        cards[i].rect.y = 100 * math.sin(10 * val - i) + offset