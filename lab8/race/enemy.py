import pygame
import random
import settings
import obstacle
import os

class Enemy(obstacle.Obstacle):
  def __init__(self):
    colors_path = "images/cars"
    colors = os.listdir(colors_path)
    super().__init__(60, 0.5, colors_path + "/" + random.choice(colors), settings.SPEED)
    self.image = pygame.transform.rotate(self.image, 180)

  def changeSpeed (self, speed):
    self.speed = speed
