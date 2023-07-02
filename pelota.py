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
        self.verticalSpeed = 5
        self.horizontalSpeed = 5
        self.strengh = 1

    def update(self,limX,limY,choquevertical = False, choqueHorizontal = False):
        
        if self.rect.right >= limX or self.rect.left <= 0 or choqueHorizontal:
            self.verticalSpeed *= -1
        if self.rect.top <= 0 or choquevertical:
            self.horizontalSpeed *= -1

        self.rect.x += self.verticalSpeed
        self.rect.y += self.horizontalSpeed
        
    def masFuerza(self):
        self.strengh = FUERZA_POWERUP 

