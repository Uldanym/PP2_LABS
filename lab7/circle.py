import pygame

pygame.init()

screen=pygame.display.set_mode((800,600))
#fps
clock=pygame.time.Clock()

white=(255,255,255)
red=(255,0,0)

x=30
y=30


done=True

while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        

    keys=pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and x<770:
        x += 20
    if keys[pygame.K_LEFT] and x>30: 
        x -= 20
    if keys[pygame.K_UP]and y>30: 
        y -= 20
    if keys[pygame.K_DOWN] and y<570: 
        y += 20

    screen.fill(white)
    pygame.draw.circle(screen, red, (x, y), 25)
    pygame.display.flip()
    clock.tick(60)
 