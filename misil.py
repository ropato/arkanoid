import pygame
import powerup

class Misille(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("resources/missile.png")
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y - self.rect.height
        self.strengh = 3
    
    def lauch(self):
        self.rect.y -= 5