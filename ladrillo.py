import pygame
import powerup

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,color,posX,posY,resistencia, puntos):
        super().__init__()
        self.image = pygame.Surface([70,20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.resistencia = resistencia
        self.puntos = puntos
        
class ladrillo_p(Ladrillo):
    def __init__(self, color, posX, posY, resistencia, puntos, powerUp):
        super().__init__(color, posX, posY, resistencia, puntos)
        self.powerUp=powerUp

        