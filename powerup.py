import pygame
class powerup (pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("resources\power1.png").convert()
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width=30
        self.rect.height=30
        self.velocidadV = 5
    