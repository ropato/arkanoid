import pygame

class Pelota(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("pelota.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidadH = 10
        self.velocidadV = 5

    def update(self,limX,limY,choquevertical = False, choqueHorizontal = False):
        
        if self.rect.right >= limX or self.rect.left <= 0 or choqueHorizontal:
            self.velocidadH *= -1
        if self.rect.top <= 0 or choquevertical:
            self.velocidadV *= -1

        self.rect.x += self.velocidadH
        self.rect.y += self.velocidadV
        