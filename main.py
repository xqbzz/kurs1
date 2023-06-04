import random
import pygame
import os
import av
import imageio
import datetime
import pygame.font

from objects import Background, Dino, Cactus, Cloud, Ptera, Star

# Инициализация Pygame
pygame.init()
SCREEN = WIDTH, HEIGHT = (600, 400) # Размеры экрана
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)

clock = pygame.time.Clock() # Отображение FPS
font = pygame.font.SysFont('Arial', 18)
FPS = 60
record = False # Флаг для записи
output_folder = "recordings"  # Папка для сохранения записей(название любое, создаст сама если нет)
video_writer = None
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

#Цвета

WHITE = (225,225,225)
BLACK = (0, 0, 0)
GRAY = (32, 33, 36)
GREEN = (0, 255, 0)

# Изображния

start_img = pygame.image.load('Dino/start_img.png')
start_img = pygame.transform.scale(start_img, (400, 400))
start_rect = start_img.get_rect()
start_rect.center = (WIDTH // 2, HEIGHT // 2)

pause_img = pygame.image.load('Dino/Button/Pause.png')
pause_img = pygame.transform.scale(pause_img, (250, 75))

game_over_img = pygame.image.load('Dino/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (200, 36))

replay_img = pygame.image.load('Dino/replay.png')
replay_img = pygame.transform.scale(replay_img, (40, 36))
replay_rect = replay_img.get_rect()
replay_rect.x = WIDTH // 2 - 20
replay_rect.y = 100

numbers_img = pygame.image.load('Dino/numbers.png')
numbers_img = pygame.transform.scale(numbers_img, (120, 12))

# Кнопки для уровней игры(Not WORKING)
button_nornal_img = pygame.image.load('Dino/Button/Normal.png')
button_hard_img = pygame.image.load('Dino/Button/Hard.png')
button_ultra_img = pygame.image.load('Dino/Button/Ultra.png')
button_selected_normal_img = pygame.image.load('Dino/Button/NormalRED.png')
button_selected_hard_img = pygame.image.load('Dino/Button/HardRED.png')
button_selected_ultra_img = pygame.image.load('Dino/Button/UltraRED.png')
# Звуки

jump_fx = pygame.mixer.Sound('Dino/Sound/jump.wav')
die_fx = pygame.mixer.Sound('Dino/Sound/die.wav')
collect_star_fx = pygame.mixer.Sound('Dino/Sound/collect_star.wav')
background_fx = pygame.mixer.Sound('Dino/Sound/background.wav')
retry_fx = pygame.mixer.Sound('Dino/Sound/retry.wav')

# Создание игровых объектов и групп

ground = Background()
dino = Dino(50, 160)

cactus_group = pygame.sprite.Group()
ptera_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()

# Создание объекта контейнера для записи видео
container = av.open(os.path.join(output_folder, "game_record.mp4"), mode='w')
video_stream = container.add_stream('libx264', rate=60)
video_stream.width = WIDTH
video_stream.height = HEIGHT

# Функции для записи видео
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

# Функция сброса игры
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

# Переменные и флаги
keys = []
GODMODE = False
DAYMODE = False
LYAGAMI = False
counter = 0
enemy_time = 120
cloud_time = 500
stars_time = 150

SPEED = 5
jump = False
duck = False

score = 0
high_score = 0

game_over = False
play_retry = False

start_page = True
mouse_pos = (-1, -1)
background_fx.set_volume(0.1)
background_fx.play(-1)

running = True
fps_text = font.render("", True, GREEN)#FPS текст( можно поменять цвет и Front)
paused = False
# Главный цикл игры
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
                        jump_fx.play()
                    else:
                        reset()

                if event.key == pygame.K_UP:
                    jump = True
                    jump_fx.play()

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
    
    # Отображение стартовой страницы    
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
                    type = random.randint(1, 9)
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
                        die_fx.play()

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
                        die_fx.play()
					
		# Расчет и отображение FPS
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {int(fps)}", True, GREEN)

        if paused:
            win.blit(pause_img, (180, 200))  # Отображение изображения start_img
            pygame.display.update()
            continue  # Пропуск обновления игры в режиме паузы
        
		# Обновление и отображение объектов
        ground.update(SPEED)
        ground.draw(win)
        cloud_group.update(SPEED - 3, dino)
        cloud_group.draw(win)
        stars_group.update(SPEED - 3, dino,score)
        for star in stars_group:
            if pygame.sprite.collide_rect(dino, star):
                star.kill()
                collect_star_fx.play()
                score += 50  
        stars_group.draw(win)
        cactus_group.update(SPEED, dino)
        cactus_group.draw(win)
        ptera_group.update(SPEED - 1, dino)
        ptera_group.draw(win)
        dino.update(jump, duck)
        dino.draw(win)

        # Отображение счета и рекорда
        string_score = str(score).zfill(5)
        for i, num in enumerate(string_score):
            win.blit(numbers_img, (520 + 11 * i, 10), (10 * int(num), 0, 10, 12))

        if high_score:
            win.blit(numbers_img, (425, 10), (100, 0, 20, 12))
            string_score = f'{high_score}'.zfill(5)
            for i, num in enumerate(string_score):
                win.blit(numbers_img, (455 + 11 * i, 10), (10 * int(num), 0, 10, 12))
        
        # Обработка конца игры и возможности перезапуска
        if not dino.alive:
            win.blit(game_over_img, (WIDTH // 2 - 100, 55))
            win.blit(replay_img, replay_rect)
            retry_fx.set_volume(0.05)
            if not play_retry:  
                retry_fx.play()
                play_retry_fx = True  
            game_over = True  
            
        if replay_rect.collidepoint(mouse_pos):
            reset()


    # Вывод FPS на экран
    win.blit(fps_text, (10, 10))
    pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 4)
    clock.tick(FPS)
    pygame.display.update()

    # Запись кадра в видеофайл, если флаг записи активен
    if record:
        frame = pygame.surfarray.array3d(win).swapaxes(0, 1)
        packet = av.VideoFrame.from_ndarray(frame, format='rgb24')
        packet = video_stream.encode(packet)
        container.mux(packet)

pygame.quit()
container.close()