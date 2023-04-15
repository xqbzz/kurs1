import pygame

WIDTH = 600
HEIGHT = 200
SCREEN = WIDTH, HEIGHT

background = pygame.image.load('Dino/bg.png')


class Background():
    def __init__(self):
        self.image = pygame.image.load('Dino/bg.png')
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
    def __init__(self, x, y):
        self.x, self.base = x, y

        self.run_list = []
        self.duck_list = []

        for i in range(1, 4):
            dino_img = pygame.image.load(f'Dino/Dino/{i}.png')
            dino_img = pygame.transform.scale(dino_img, (52, 58))
            self.run_list.append(dino_img)

        for i in range(4, 6):
            dino_img = pygame.image.load(f'Dino/Dino/{i}.png')
            dino_img = pygame.transform.scale(dino_img, (70, 38))
            self.duck_list.append(dino_img)

        self.dead_image = pygame.image.load(f'Dino/Dino/8.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (52, 58))

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
            elif self.isJumping:
                self.index = 0
                self.counter = 0
                self.image = self.run_list[self.index]
            else:
                self.counter += 1
                if self.counter >= 4:
                    self.index = (self.index + 1) % len(self.run_list)
                    self.image = self.run_list[self.index]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x
                    self.rect.bottom = self.base
                    self.counter = 0

            self.mask = pygame.mask.from_surface(self.image)

        else:
            self.image = self.dead_image

    def draw(self, win):
        win.blit(self.image, self.rect)


class Cactus(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Cactus, self).__init__()

        self.image_list = []
        for i in range(5):
            scale = 0.65
            img = pygame.image.load(f'Dino/Cactus/{i + 1}.png')
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
            self.image_list.append(img)

        self.image = self.image_list[type - 1]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.bottom = 165

    def update(self, speed, dino):
        if dino.alive:
            self.rect.x -= speed
            if self.rect.right <= 0:
                self.kill()

            self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, self.rect)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Cloud, self).__init__()
        self.image = pygame.image.load(f'Dino/cloud.png')
        self.image = pygame.transform.scale(self.image, (60, 18))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed, dino):
        if dino.alive:
            self.rect.x -= speed
            if self.rect.right <= 0:
                self.kill()

    def draw(self, win):
        win.blit(self.image, self.rect)


class Ptera(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Ptera, self).__init__()

        self.image_list = []
        for i in range(2):
            scale = 0.65
            img = pygame.image.load(f'Dino/Ptera..')
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * scale)), int(h * scale))
            self.image_list.append(img)

        self.index = 0
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(center=(x, y))

        self.counter = 0

    def update(self, speed, dino):
        if dino.alive:
            self.rect.x -= speed
            if self.rect.right <= 0:
                self.kill()

            self.counter += 1
            if self.counter >= 6:
                self.index = (self.index + 1) % len(self.image_list)
                self.image = self.image_list[self.index]
                self.counter = 0

            self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, self.rect)


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super(Star, self).__init__()
        image = pygame.image.load(f'Dino/stsrs.png')
        self.image_list = []
        for i in range(3):
            img = image.subsurface((0, 20 * (i), 18, 18))
            self.image_list.append(img)
        self.image = self.image_list[type - 1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, speed, dino):
        if dino.alive:
            self.rect.x -= speed
            if self.rect.right <= 0:
                self.kill()

    def draw(self, win):
        win.blit(self.image, self.rect)
