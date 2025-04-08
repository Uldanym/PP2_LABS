import pygame


pygame.init()

nauryzDumanPath=r"C:\Users\Lenovo\Desktop\PP2\lab7\roza-rymbaeva_-_nauryz-duman.mp3"
despacitoPath=r"C:\Users\Lenovo\Desktop\PP2\lab7\Luis Fonsi feat. Daddy Yankee - Despacito.mp3"
kazakhAnuranPath=r"C:\Users\Lenovo\Desktop\PP2\lab7\Қазақстан - Әнұран.mp3"

screen=pygame.display.set_mode((406,600))
pygame.display.set_caption("MP3 PLAYER")
#fps
clock=pygame.time.Clock()
image=pygame.image.load(r"C:\Users\Lenovo\Desktop\PP2\lab7\player.png")
image = pygame.transform.scale(image, (406, 600))

musicList = [nauryzDumanPath, despacitoPath, kazakhAnuranPath]
pygame.mixer.music.load(musicList[0]) 

pygame.mixer.music.play(-1)

Play=True
running=True

musicNames = ["Nauryz Duman", "Despacito", "Kazakh Anuran"]

font = pygame.font.SysFont(None, 36)

index=0
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
             running=False
             
    
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                Play=not Play
                
                if Play:
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.pause() 
                    
            elif event.key==pygame.K_RIGHT:
                index+=1
                if index==len(musicList):
                    index=0
                pygame.mixer.music.load(musicList[index])   
                pygame.mixer.music.play() 
                
            elif event.key==pygame.K_LEFT:
                index-=1
                if index==-1:
                    index=len(musicList)-1
                pygame.mixer.music.load(musicList[index])   
                pygame.mixer.music.play()  
    screen.blit(image,(0,0))
    pygame.draw.rect(screen, (0, 0, 0), (20, 20, 200, 40))
    text_surface = font.render(musicNames[index], True, (255, 255, 255))
    screen.blit(text_surface, (20, 20))
                
    pygame.display.flip()   
    clock.tick(60)