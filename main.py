import random
import pygame

from objects import Background, Dino, Cactus, Cloud, Ptera, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (1920, 720)
win = pygame.display.set_made(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60