import random
import pygame

from objects import Background, Dino, Cactus, Cloud, Ptera, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 400)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

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
start_img = pygame.transform.scale(start_img, (80,80))

game_over_img = pygame.image.load('Dino/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200,36))

replay_img = pygame.image.load('Dino/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 -30
replay_rect.y = 100

numbers_img = pygame.image.load('Dino/numbers.png')
numbers_img = pygame.transform.scale(numbers_img,(120,12))

#МУЗЫКА(СДЕЛАТЬ)
#
#
#
#

#ОБЪЕКТЫ
ground = Background()
dino = Dino(100, 100)

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

    dino.reset()

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
while running:
    jump = False
    duck = False  
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
        
            if event.key == pygame.K_SPACE: 
                if start_page:
                    start_page = False
                elif dino.alive:
                    jump = True
                    #SOUND
                else:
                    reset()
                
            if event.key == pygame.K_DOWN:     
                duck = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump = False

            if event.key == pygame.K_DOWN:
                duck = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = (-1, -1)


    if start_page:
        win.blit(start_img, (50, 100))
    else:
        if dino.alive:
            counter +=1
            if counter % int(enemy_time) == 0:
                if random.randint(1, 10) == 5:
                    y = random.choice([85, 130])
                    ptera = Ptera(WIDTH, y)
                    ptera_group.add(ptera)
                else:
                    type = random.randint(1,4)
                    cactus = Cactus(type)
                    cactus_group.add(cactus)

            if counter % cloud_time == 0:
                y = random.randint(100,100)
                cloud = Cloud(WIDTH, y)
                cloud_group.add(cloud)
            
            if counter % stars_time == 0:
                type = random.randint(1,3)
                y = random.randint(40, 100)
                star = Star(WIDTH, y, type)
                stars_group.add(star)

            if counter % 100 == 0:
                SPEED += 0.1
                enemy_time -= 0.5

            if counter % 5 == 0:
                score +=1

            '''if score and score % 100 == 0:
                #MUSIC'''

        ground.update(SPEED)
        ground.draw(win)
        cloud_group.update(SPEED-3, dino)
        cloud_group.draw(win)
        stars_group.update(SPEED-3,dino)
        stars_group.draw(win)
        cactus_group.update(SPEED, dino)
        cactus_group.draw(win)
        ptera_group.update(SPEED-2, dino)
        ptera_group.draw(win)
        dino.update(jump, duck)
        dino.draw

        string_score = str(score).zfill(5)
        for i, num in enumerate(string_score):
            win.blit(numbers_img,(520+11*i,10),(10*int(num), 0, 10, 12))

        if high_score:
            win.blit(numbers_img,(425,10),(100,0,20,12))
            string_score = f'{high_score}'.zfill(5)
            for i, num in enumerate(string_score):
                win.blit(numbers_img, (455+11*i,10))
        
        if not dino.alive:
            win.blit(game_over_img,(WIDTH//2-100,55))
            win.blit(replay_img, replay_rect)

            if replay_rect.collidedict(mouse_pos):
                reset()

    pygame.draw.rect(win,WHITE,(0,0,WIDTH,HEIGHT),4)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()