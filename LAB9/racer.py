import pygame
import time
import random

pygame.init()

# Окно игры
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

# Загрузка изображений
image_background = pygame.image.load(r"C:\Users\Lenovo\Desktop\PP2\LAB8\AnimatedStreet.png")
image_player = pygame.image.load(r"C:\Users\Lenovo\Desktop\PP2\LAB8\Player.png")
image_enemy = pygame.image.load(r"C:\Users\Lenovo\Desktop\PP2\LAB8\Enemy.png")
image_coin = pygame.image.load(r"C:\Users\Lenovo\Desktop\PP2\LAB8\pngimg.com - coin_PNG36871.png")
image_coin = pygame.transform.scale(image_coin, (30, 30)) 



# Музыка и звуки
pygame.mixer.music.load(r"C:\Users\Lenovo\Desktop\PP2\LAB8\background.wav") 
pygame.mixer.music.play(-1) 
sound_crash = pygame.mixer.Sound(r"C:\Users\Lenovo\Desktop\PP2\LAB8\crash.wav")


# Шрифты
font = pygame.font.SysFont("Verdana", 60)
small_font = pygame.font.SysFont("Verdana", 20)
image_game_over = font.render("Game Over", True, "black")

# Параметры фона
background_y = 0
scroll_speed = 5
score = 0
N = 10  

# Определяем разные размеры и "ценность" монет
COIN_SIZES = [(20, 1), (30, 3), (40, 5)]  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size, self.value = random.choice(COIN_SIZES)  
        self.image = pygame.transform.scale(image_coin, (size, size))
        self.rect = self.image.get_rect(
            center=(random.randint(30, WIDTH - 30), random.randint(0, HEIGHT // 3))
        )
        self.speed = scroll_speed

    def move(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH - 50), 0))
        self.base_speed = random.randint(5, 10)
        self.speed_multiplier = speed_multiplier  

    def move(self):
        self.rect.y += self.base_speed * self.speed_multiplier 
        if self.rect.top > HEIGHT:
            self.kill()

# Создание объектов
player = Player()
all_sprites = pygame.sprite.Group(player)
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

running = True
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()

    # Прокрутка фона
    background_y = (background_y + scroll_speed) % HEIGHT
    screen.blit(image_background, (0, background_y - HEIGHT))
    screen.blit(image_background, (0, background_y))

    # Генерация объектов
    frame_count += 1
    if frame_count % 50 == 0:
        new_coin = Coin()
        coin_sprites.add(new_coin)
        all_sprites.add(new_coin)

    if frame_count % 100 == 0:
        speed_multiplier = 1 + (score // N) * 0.2  
        new_enemy = Enemy(speed_multiplier)
        enemy_sprites.add(new_enemy)
        all_sprites.add(new_enemy)

    # Движение и отображение объектов
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    # Проверка столкновения с монетами
    collected_coins = pygame.sprite.spritecollide(player, coin_sprites, True)
    score += sum(coin.value for coin in collected_coins)  

    # Проверка столкновения с врагами
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        running = False
        screen.fill("red")
        screen.blit(image_game_over, (30, 250))
        pygame.display.flip()
        time.sleep(3)

    # Отображение счета
    score_text = small_font.render(f"Coins: {score}", True, "black")
    screen.blit(score_text, (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit() 