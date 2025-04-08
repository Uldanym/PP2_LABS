import pygame 
import time   
import random 

pygame.init() 

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




class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = image_player 
        self.rect = self.image.get_rect() 
        self.rect.x = WIDTH // 2 - self.rect.w // 2 
        self.rect.y = HEIGHT - self.rect.h 
        self.speed = 5 

    def move(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0) 
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        # Ограничения движения
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = self.rect.h   


class Coin(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, WIDTH-30) 
        self.rect.y = random.randint(0, HEIGHT // 3)  
        self.speed = scroll_speed  
        
    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill() 


   

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width) 
        self.rect.y = 0 
        self.speed = random.randint(5, 10)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()


# Создание объектов
player = Player()
all_sprites = pygame.sprite.Group() 
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group() 

all_sprites.add(player)

# Запускаем игру
running = True
frame_count = 0  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()

    # Прокрутка фона
    background_y += scroll_speed 
    if background_y >= HEIGHT: 
        background_y = 0

    screen.blit(image_background, (0, background_y - HEIGHT))
    screen.blit(image_background, (0, background_y))

    



    # Генерация новых монет и машин
    frame_count += 1 
    if frame_count % 50 == 0:  
        new_coin = Coin(player)
        coin_sprites.add(new_coin)
        all_sprites.add(new_coin)

    if frame_count % 100 == 0:  
        new_enemy = Enemy() 
        enemy_sprites.add(new_enemy)
        all_sprites.add(new_enemy)

    # Движение объектов
    for entity in all_sprites: 
        entity.move() 
        screen.blit(entity.image, entity.rect) 



    # Проверка столкновения с монетами
    collected_coins = pygame.sprite.spritecollide(player, coin_sprites, True)
    score += len(collected_coins)

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
