import random
import pygame

from objects import Background, Dino, Cactus, Cloud, Ptera, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (1920, 720)
win = pygame.display.set_mode(SCREEN, pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

#ЦВЕТ

WHITE = (225,225,225)
BLACK = ( 0, 0, 0)
GRAY = (32, 33, 36)
GREENYELLOW = (173,255,47)
GREEN = ( 0, 100, 0)
#......
#ВЫВОД КАРТИНОК
start_img = pygame.image.load('Dino/start_img.png')
start_img = pygame.transform.scale(start_img, (60,64))

game_over_img = pygame.image.load('Dino/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200,36))

replay_img = pygame.image.load('Dino/ replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 -30
replay_rect.y = 100

#МУЗЫКА(СДЕЛАТЬ)
#
#
#
#

#ОБЪЕКТЫ
ground = Background()
dino = Dino(50, 160)

cactus_group = pygame.sprite.Group()
ptera_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()

#FUNC

def reset():
    global counter, SPEED, score, high_score

    if score and score >= high_score:
        high_score = score

    counter = 0
    SPEED = 5
    score = 0

    cactus_group.empty()
    ptera_group.empty()
    cloud_group.empty()
    stars_group.empty()

    dino.reset

counter = 0
enemy_time = 100
cloud_time = 500
stars_time = 175

SPEED = 5
jump = False
duck = False

score = 0
high_score = 0

start_page = True
mouse_pos = (-1, -1)

running = True