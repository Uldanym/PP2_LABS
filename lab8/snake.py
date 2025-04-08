import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

CELL = 30 


font = pygame.font.SysFont("Verdana", 20)

def draw_grid(): 
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)] 
        self.dx = 1 
        self.dy = 0 
        self.score = 0
        self.level = 1
        self.speed = 5


    def move(self):
        
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
            
        
        self.body[0].x += self.dx
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
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            self.score += 1
            food.generate_random_pos()

            
            if self.score % 3 == 0:
                self.level += 1
                self.speed += 1

class Food:
    def __init__(self):
        self.pos = Point(9, 9) 

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self): 
        self.pos.x = random.randint(0, WIDTH // CELL - 1)
        self.pos.y = random.randint(0, HEIGHT // CELL - 1)
        

clock = pygame.time.Clock()


food = Food()
snake = Snake()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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

    screen.fill(colorBLACK)
    draw_grid()
    snake.move()
    snake.check_collision(food)
    snake.draw()
    food.draw()


    score_text = font.render(f"Score: {snake.score}", True, colorWHITE)
    level_text = font.render(f"Level: {snake.level}", True, colorWHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    

    pygame.display.flip()
    clock.tick(snake.speed) 



pygame.quit()
