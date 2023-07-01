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
        self.velocidadH = 5
        self.velocidadV = 5
        self.fuerza = 1

    def update(self,limX,limY,choquevertical = False, choqueHorizontal = False):
        
        if self.rect.right >= limX or self.rect.left <= 0 or choqueHorizontal:
            self.velocidadH *= -1
        if self.rect.top <= 0 or choquevertical:
            self.velocidadV *= -1

        self.rect.x += self.velocidadH
        self.rect.y += self.velocidadV
        
    def masFuerza(self):
        self.fuerza = FUERZA_POWERUP 

