import random
import pygame
import os
import av
import imageio
import datetime

from objects import Background, Dino, Cactus, Cloud, Ptera, Star

pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 400)
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock()
FPS = 60
record = False
output_folder = "recordings"  # Папка для сохранения записей(название любое)
video_writer = None
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# COLORS *********************************************************************

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)

# IMAGES *********************************************************************

start_img = pygame.image.load('Dino/start_img.png')
start_img = pygame.transform.scale(start_img, (400, 400))
start_rect = start_img.get_rect()
start_rect.center = (WIDTH // 2, HEIGHT // 2)

game_over_img = pygame.image.load('Dino/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

replay_img = pygame.image.load('Dino/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 100

numbers_img = pygame.image.load('Dino/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

button_nornal_img = pygame.image.load('Dino/Button/Normal.png')
button_hard_img = pygame.image.load('Dino/Button/Hard.png')
button_ultra_img = pygame.image.load('Dino/Button/Ultra.png')
button_selected_normal_img = pygame.image.load('Dino/Button/NormalRED.png')
button_selected_hard_img = pygame.image.load('Dino/Button/HardRED.png')
button_selected_ultra_img = pygame.image.load('Dino/Button/UltraRED.png')
# SOUNDS *********************************************************************

#jump_fx = pygame.mixer.Sound('Sounds/jump.wav')
#die_fx = pygame.mixer.Sound('Sounds/die.wav')
#checkpoint_fx = pygame.mixer.Sound('Sounds/checkPoint.wav')

# OBJECTS & GROUPS ***********************************************************

ground = Background()
dino = Dino(50, 160)

cactus_group = pygame.sprite.Group()
ptera_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()

container = av.open(os.path.join(output_folder, "game_record.mp4"), mode='w')
video_stream = container.add_stream('libx264', rate=60)
video_stream.width = WIDTH
video_stream.height = HEIGHT

button_normal_pos = (100, 100)
button_hard_pos = (200, 100)
button_ultra_pos = (300, 100)

# FUNCTIONS ******************************************************************
def start_record():
    global record, video_writer
    record = True
    screen_size = (WIDTH, HEIGHT)
    current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # Генерация строки с текущей датой и временем
    video_filename = os.path.join(output_folder, f"game_record_{current_datetime}.mp4")
    video_writer = imageio.get_writer(video_filename, fps=60)

def stop_record():
    global record, video_writer
    record = False
    video_writer.close()

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

keys = []
GODMODE = False
DAYMODE = False
LYAGAMI = False
counter = 0
enemy_time = 80
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
paused = False
while running:
    jump = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_r:
                if not record:
                    start_record()
                else:
                    stop_record()

            if event.key == pygame.K_p:
                paused = not paused

            if not paused:
                if event.key == pygame.K_SPACE:
                    if start_page:
                        start_page = False
                    elif dino.alive:
                        jump = True
                        # jump_fx.play()
                    else:
                        reset()

                if event.key == pygame.K_UP:
                    jump = True
                    # jump_fx.play()

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
        win.blit(start_img, (100, 0))
    else:
        if dino.alive and not paused:
            counter += 1
            if counter % int(enemy_time) == 0:
                if random.randint(1, 10) == 5:
                    y = random.choice([85, 130])
                    ptera = Ptera(WIDTH, y)
                    ptera_group.add(ptera)
                else:
                    type = random.randint(1, 4)
                    cactus = Cactus(type)
                    cactus_group.add(cactus)

            if counter % cloud_time == 0:
                y = random.randint(40, 100)
                cloud = Cloud(WIDTH, y)
                cloud_group.add(cloud)

            if counter % stars_time == 0:
                type = random.randint(1, 3)
                y = random.randint(40, 100)
                star = Star(WIDTH, y, type)
                stars_group.add(star)

            if counter % 100 == 0:
                SPEED += 0.1
                enemy_time -= 0.5

            if counter % 5 == 0:
                score += 1

            if not GODMODE:
                for cactus in cactus_group:
                    if LYAGAMI:
                        dx = cactus.rect.x - dino.rect.x
                        if 0 <= dx <= (70 + (score // 100)):
                            jump = True

                    if pygame.sprite.collide_mask(dino, cactus):
                        SPEED = 0
                        dino.alive = False
                        # die_fx.play()

                for cactus in ptera_group:
                    if LYAGAMI:
                        dx = ptera.rect.x - dino.rect.x
                        if 0 <= dx <= 70:
                            if dino.rect.top <= ptera.rect.top:
                                jump = True
                            else:
                                duck = True
                        else:
                            duck = False

                    if pygame.sprite.collide_mask(dino, ptera):
                        SPEED = 0
                        dino.alive = False
                        # die_fx.play()

        if paused:
            win.blit(start_img, (100, 0))  # Отображение изображения start_img
            pygame.display.update()
            continue  # Пропуск обновления игры в режиме паузы

        ground.update(SPEED)
        ground.draw(win)
        cloud_group.update(SPEED - 3, dino)
        cloud_group.draw(win)
        stars_group.update(SPEED - 3, dino)
        stars_group.draw(win)
        cactus_group.update(SPEED, dino)
        cactus_group.draw(win)
        ptera_group.update(SPEED - 1, dino)
        ptera_group.draw(win)
        dino.update(jump, duck)
        dino.draw(win)

        string_score = str(score).zfill(5)
        for i, num in enumerate(string_score):
            win.blit(numbers_img, (520 + 11 * i, 10), (10 * int(num), 0, 10, 12))

        if high_score:
            win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
            string_score = f'{high_score}'.zfill(5)
            for i, num in enumerate(string_score):
                win.blit(numbers_img, (455 + 11 * i, 10), (10 * int(num), 0, 10, 12))

        if not dino.alive:
            win.blit(game_over_img, (WIDTH // 2 - 100, 55))
            win.blit(replay_img, replay_rect)

            if replay_rect.collidepoint(mouse_pos):
                reset()

    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
    clock.tick(FPS)
    pygame.display.update()

    if record:
        frame = pygame.surfarray.array3d(win).swapaxes(0, 1)
        packet = av.VideoFrame.from_ndarray(frame, format='rgb24')
        packet = video_stream.encode(packet)
        container.mux(packet)

pygame.quit()
container.close()