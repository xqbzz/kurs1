import pygame
import math

SCREEN = WIDTH, HEIGHT = (600, 400)

class Background():
    def __init__(self):
        self.image = pygame.image.load('Dino/bg1.png')
        self.rect = self.image.get_rect()
        self.width = 600
        self.height = 400
        self.ratio = WIDTH / self.width
        self.scaled_width = int(self.width * self.ratio)
        self.scaled_height = int(self.height * self.ratio)
        self.x1 = 0
        self.x2 = self.scaled_width
        self.y = 0


    def update(self, speed):
        self.x1 -= int(speed * self.ratio)
        self.x2 -= int(speed * self.ratio)
        if self.x1 <= -self.scaled_width:
            self.x1 = self.scaled_width
        if self.x2 <= -self.scaled_width:
            self.x2 = self.scaled_width
    def draw(self, win):
        win.blit(pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height)), (self.x1, self.y))
        win.blit(pygame.transform.scale(self.image, (self.scaled_width, self.scaled_height)), (self.x2, self.y))


class Dino():
	def __init__(self, x, y):
		self.x, self.base = x, 385

		self.run_list = []
		self.duck_list = []

		for i in range(1, 4):
			img = pygame.image.load(f'DIno/Dino/{i}.png')
			img = pygame.transform.scale(img, (52, 58))
			self.run_list.append(img)

		for i in range(4, 6):
			img = pygame.image.load(f'Dino/Dino/{i}.png')
			img = pygame.transform.scale(img, (70, 38))
			self.duck_list.append(img)

		self.dead_image = pygame.image.load(f'Dino/Dino/8.png')
		self.dead_image = pygame.transform.scale(self.dead_image, (52,58))

		self.reset()

		self.vel = 0
		self.gravity = 1
		self.jumpHeight = 15
		self.isJumping = False
		self.score = 0

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
					self.rect.x = self.x
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

	def collect_star(self):
		self.score += 50

	def draw(self, win):
		win.blit(self.image, self.rect)


class Cactus(pygame.sprite.Sprite):
	def __init__(self, type):
		super(Cactus, self).__init__()

		self.image_list = []
		for i in range(8):
			scale = 0.75
			img = pygame.image.load(f'DIno/Cactus/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
			self.image_list.append(img)

		self.image = self.image_list[type-1]
		self.rect = self.image.get_rect()
		self.rect.x = WIDTH + 10
		self.rect.bottom = 385

	def update(self, speed, dino):
		if dino.alive:
			self.rect.x -= speed
			if self.rect.right <= 0:
				self.kill()

			self.mask = pygame.mask.from_surface(self.image)

	def draw(self, win):
		win.blit(self.image, self.rect)


class Ptera(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Ptera, self).__init__()

		self.image_list = []
		for i in range(2):
			scale = 0.65
			img = pygame.image.load(f'DIno/Ptera/{i+1}.png')
			w, h = img.get_size()
			img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
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


class Cloud(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Cloud, self).__init__()
		self.image = pygame.image.load(f'DIno/cloud.png')
		self.image = pygame.transform.scale(self.image, (90, 30))
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

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super(Star, self).__init__()
        image = pygame.image.load(f'Dino/stars.png')
        self.image_list = []
        for i in range(3):
            img = image.subsurface((0, 20*(i), 18, 18))
            self.image_list.append(img)
        self.image = self.image_list[type-1]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = 0

    def update(self, speed, dino, score):
        if dino.alive:
            self.rect.x -= speed
            angle = 45  # Угол наклона (в градусах)
            radians = math.radians(angle)
            self.rect.y += int(speed * math.sin(radians))
            if self.rect.y > HEIGHT:
                self.kill()
            if pygame.sprite.collide_mask(dino, self):
                self.kill()
                score += 50  # Увеличение счета на 50 очков
		
def draw(self, win):
	win.blit(self.image, self.rect)