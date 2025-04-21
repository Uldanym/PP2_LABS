import pygame
from color_palette import *
import random
import time
import psycopg2

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont("Verdana", 20)

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="220507",
    port="5432"
)

cur = conn.cursor() #conn — это соединение с базой данных. cursor — это как ручка, которой ты пишешь и читаешь данные из этой базы.ты создаёшь инструмент, с помощью которого можно:отправлять SQL-запросы в базу (например: SELECT, INSERT, UPDATE),получать данные из базы (fetchone(), fetchall() и т.д.).

#cur.execute(...) — ты отправляешь запрос.
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username VARCHAR(255) PRIMARY KEY,
        current_level INT DEFAULT 1
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS user_scores (
        username VARCHAR(255),
        score INTEGER,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (username) REFERENCES users(username) 
    );
""")#Связь через FOREIGN KEY — нельзя сохранить результат, если такого игрока нет в таблице users.
conn.commit()#Он сохраняет изменения в базе данных.


def draw_grid():#Эта функция рисует сетку на экране игры, как поле в тетрадке.
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

class Point:#Это простой объект, который хранит координаты X и Y — точку на игровом поле.
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Food:
    def __init__(self):
        self.generate_random_food()
    
    def generate_random_food(self):
        self.pos = Point(random.randint(0, WIDTH // CELL - 1), random.randint(0, HEIGHT // CELL - 1))
        self.weight = random.choice([1, 2, 3])
        self.color = [colorGREEN, colorBLUE, colorRED][self.weight - 1]
        self.spawn_time = time.time()#Запоминается момент, когда еда появилась.
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
    
    def is_expired(self, timeout=7):
        return time.time() - self.spawn_time > timeout #time.time() — текущее время в секундах (с начала эпохи). self.spawn_time — время, когда еда была создана.

class Snake:
    def __init__(self, level=1):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = level
        self.speed = 5 + (level - 1)
        
    def is_self_collision(self):
        head = self.body[0] #берём координаты головы.
        for segment in self.body[1:]: #перебираем все остальные сегменты тела.
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

     
    def move(self):
        for i in range(len(self.body) - 1, 0, -1):#еперь каждый сегмент тела перемещается на место предыдущего сегмента.
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx #Двигаем голову змейки
        self.body[0].y += self.dy
        
        if self.body[0].x > WIDTH // CELL - 1:
            self.body[0].x = 0
        if self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y > HEIGHT // CELL - 1:
            self.body[0].y = 0
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1
    
    def draw(self):
        pygame.draw.rect(screen, colorRED, (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))
    
    def check_collision(self, food):
        if self.body[0].x == food.pos.x and self.body[0].y == food.pos.y:
            for i in range(food.weight):
                self.body.append(Point(self.body[-1].x, self.body[-1].y))
            self.score += food.weight
            food.generate_random_food()
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 1

clock = pygame.time.Clock()
food = Food()#Здесь создаётся объект класса Food, который будет представлять еду на экране.
running = True

username = input("Enter your username: ")

cur.execute("SELECT * FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if user is None:
    cur.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    conn.commit()
    level = 1
    print("New user created!")
else:
    level = user[1]
    print(f"Welcome back, {username}! Your current level is {level}.")

snake = Snake(level)  # <-- теперь создается после определения уровня

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cur.execute(
                    "UPDATE users SET current_level = %s WHERE username = %s",
                    (snake.level, username)#обновляется текущий уровень пользователя в базе данных.
                )
            cur.execute(
                    "INSERT INTO user_scores (username, score) VALUES (%s, %s)",
                    (username, snake.score)#сохраняется текущий счёт пользователя в таблице user_scores.
                )
            conn.commit()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx == 0:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx == 0:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy == 0:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy == 0:
                snake.dx = 0
                snake.dy = -1
            elif event.key == pygame.K_p:
                print("Game paused. Saving state...")
                cur.execute(
                    "UPDATE users SET current_level = %s WHERE username = %s",
                    (snake.level, username)#обновляется текущий уровень пользователя в базе данных.
                )
                cur.execute(
                    "INSERT INTO user_scores (username, score) VALUES (%s, %s)",
                    (username, snake.score)#сохраняется текущий счёт пользователя в таблице user_scores.
                )
                conn.commit()
                print("Game state saved.")
                paused = True
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                            paused = False

    screen.fill(colorBLACK)
    draw_grid()
    snake.move()
    

    if snake.is_self_collision():
        print("Game over! You ran into yourself.")
        cur.execute(
                    "UPDATE users SET current_level = %s WHERE username = %s",
                    (snake.level, username)#обновляется текущий уровень пользователя в базе данных.
                )
        cur.execute(
                    "INSERT INTO user_scores (username, score) VALUES (%s, %s)",
                    (username, snake.score)#сохраняется текущий счёт пользователя в таблице user_scores.
                )
        conn.commit()
        running = False
        continue

    snake.check_collision(food)
    snake.draw()
    food.draw()
    
    if food.is_expired():
        food.generate_random_food()
    
    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    
    pygame.display.flip()
    clock.tick(snake.speed)

pygame.quit()