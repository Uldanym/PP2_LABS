import pygame
import settings
import player
import enemy
import coin
import math

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    self.running = True
    self.font = pygame.font.SysFont("Courier New", 40)

    self.createBg()
    self.createEntities()
    self.createCounters()

  def createBg(self):
    self.bg = pygame.image.load("images/bg.png")
    bg_aspect_ratio = self.bg.get_width() / self.bg.get_height()
    self.bg = pygame.transform.scale(self.bg, (settings.SCREEN_WIDTH, math.ceil(settings.SCREEN_WIDTH / bg_aspect_ratio)))
    self.copies = math.ceil(settings.SCREEN_HEIGHT / self.bg.get_height()) + 1

  def drawBg(self):
    self.screen.fill(settings.WHITE)
    self.scroll = (self.scroll + self.speed // 1.5) % self.bg.get_height()
    for i in range(self.copies):
      self.screen.blit(self.bg, (0, self.scroll + (i - 1) * (self.bg.get_height() - 1)))

  def createCounters(self):
    self.scroll = 0
    self.coins = 0
    self.speed = settings.SPEED

  def drawCoinCounter(self):
    coins_counter = self.font.render(str(self.coins), True, settings.BLACK)
    pygame.draw.rect(self.screen, settings.WHITE, (settings.SCREEN_WIDTH - 60, 0, 60, 60))
    self.screen.blit(coins_counter, (settings.SCREEN_WIDTH - 50, 10))

  def createEntities(self):
    self.player = player.Player()
    self.enemy = enemy.Enemy()
    self.coin = coin.Coin()

  def drawEntities(self):
    self.player.draw(self.screen)
    self.enemy.draw(self.screen)
    self.coin.draw(self.screen)
    self.player.move()
    self.enemy.move()
    self.coin.move()

  def watchCollisions(self):
    if(self.player.rect.colliderect(self.enemy.rect)):
      self.screen.fill(settings.RED)
      self.running = False

    if(self.player.rect.colliderect(self.coin.rect)):
      self.coin.__init__()
      self.coins += 1

    if(self.enemy.rect.colliderect(self.coin.rect)):
      self.coin.__init__()

  def watchEvents(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False

  def run(self):
    clock = pygame.time.Clock()
    while self.running:
      self.watchEvents()
      self.watchCollisions()
      self.drawBg()
      self.drawEntities()
      self.drawCoinCounter()
      pygame.display.flip()
      clock.tick(settings.FPS)