import pygame

class Entity:
  def __init__(self, width, aspect_ratio, image_path, speed):
    self.width = width
    self.aspect_ratio = aspect_ratio
    self.height = self.width / self.aspect_ratio

    self.image = pygame.image.load(image_path)
    self.image = pygame.transform.scale(self.image, (self.width, self.height))
    self.rect = self.image.get_rect()
    self.MOVEMENT_SPEED = speed

  def draw(self, screen):
    screen.blit(self.image, self.rect)
    