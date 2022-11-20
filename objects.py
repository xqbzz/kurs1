import pygame

SCREEN = WIDTH, HEIGHT = (600, 200)

background = pygame.image.load('Dino/bg.png')


class Background():
    def __init__(self):
        self.image = pygame.image.load('Dino/ground.png')
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = 150

    def update(self, speed):
        self.x1 -= speed
        self.x2 -= speed
        if self.x1 <= -self.width:
            self.x1 = self.width
        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))


class Dino():
    def __init__(self,x,y):
        self.x, self.base = x, y

        self.run_list = []
        self.duck_list = []

        for i in range(1,4):
            dino_img = pygame.image.load(f'Dino/Dino/{i}.png')
            dino_img = pygame.transform.scale(dino_img, (52,58))
            self.run_list.append(dino_img)

        for i in range (4,6):
            dino_img = pygame.image.load(f'Dino/Dino/{i}.png')
            dino_img = pygame.transform.scale(dino_img, (70,38))
            self.duck_list.append(dino_img)

        self.dead_image = pygame.image.load(f'Dino/Dino/8.png')
        self.dead_image = pygame.transform.scale(self.dead_image,(52,58))

        self.reset()

        self.vel = 0
        self.gravity = 1
        self.jumpHeight = 15
        self.isJumping = False

    def reset(self):
        self.index = 0
        self.image = self.run_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.bottom = self.base

        self.alive = True
        self.counter = 0

    def update(self, jump, duck):
        if self.alive:
            if not self.isJumping and jump:
                self.vel = -self.jumpHeight
                self.isJumping = True

            self.vel += self.gravity
            if self.vel >= self.jumpHeight:
                self.vel = self.jumpHeight

            self.rect.y += self.vel
            if self.rect.bottom > self.base:
                self.rect.bottom = self.base
                self.isJumping = False

            if duck:
                self.counter += 1
                if self.counter >= 6:
                    self.index = (self.index + 1) % len(self.duck_list)
                    self.image = self.duck_list[self.index]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x = self.x
                    self.rect.bottom = self.base
                    self.counter = 0




