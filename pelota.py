import pygame
import threading
FUERZA_POWERUP = 30
class Pelota(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("resources/pelotaDVD.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.verticalSpeed = -5
        self.horizontalSpeed = 5
        self.strengh = 1
        self.bounce = pygame.mixer.Sound("resources/rebotePelota.mp3")

    def invertVSpeed(self):
        self.verticalSpeed*= -1
    def invertHSpeed(self):
        self.horizontalSpeed*= -1
    def move(self):
        self.rect.x += self.horizontalSpeed
        self.rect.y += self.verticalSpeed
    def strengthUp(self):
        self.strengh = FUERZA_POWERUP 

