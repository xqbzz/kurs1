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
