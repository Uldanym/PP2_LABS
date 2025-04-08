import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
COLOR_BUTTONS = [(10 + i * 40, 10, 30, 30) for i in range(len(COLORS))]

SHAPES = ["draw", "rect", "circle", "eraser", "line"]
SHAPE_BUTTONS = [(200 + i * 80, 10, 70, 30) for i in range(len(SHAPES))]

current_color = BLACK
mode = "draw"
start_pos = None
last_pos = None
brush_size = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint in Pygame")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

def draw_ui():
    for i, rect in enumerate(COLOR_BUTTONS):
        pygame.draw.rect(screen, COLORS[i], rect)
    for i, rect in enumerate(SHAPE_BUTTONS):
        pygame.draw.rect(screen, (200, 200, 200), rect)
        font = pygame.font.Font(None, 24)
        text = font.render(SHAPES[i], True, (0, 0, 0))
        screen.blit(text, (rect[0] + 5, rect[1] + 5))

running = True
while running:
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    draw_ui()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for i, rect in enumerate(COLOR_BUTTONS):
                if pygame.Rect(rect).collidepoint(x, y):
                    current_color = COLORS[i]
            for i, rect in enumerate(SHAPE_BUTTONS):
                if pygame.Rect(rect).collidepoint(x, y):
                    mode = SHAPES[i]
            start_pos = event.pos
            last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            end_pos = event.pos
            if mode == "rect":
                pygame.draw.rect(canvas, current_color, pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])), 2)
            elif mode == "circle":
                radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(canvas, current_color, start_pos, radius, 2)
            elif mode == "line":
                pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)
        elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
            if mode == "draw":
                pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                pygame.draw.circle(canvas, current_color, event.pos, brush_size // 2)
                last_pos = event.pos
            elif mode == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, event.pos, 15)
                pygame.draw.circle(canvas, WHITE, event.pos, 5)
                last_pos = event.pos
    
    pygame.display.flip()

pygame.quit()
sys.exit()
