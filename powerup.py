import pygame
SPRITE_SIZE = (50, 50)
class powerUp (pygame.sprite.Sprite):
    def __init__(self,x,y, powerUp):
        super().__init__()
        self.image = pygame.image.load("resources/power1.png").convert()
        self.image = pygame.transform.scale(self.image,SPRITE_SIZE)
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.powerUp = powerUp
        self.velocidadV = 3

    # def onHit(self):
    #     self.image = pygame.transform.smoothscale(self.image,(50, 50))
    def fallDown(self):
        self.rect.y+= self.velocidadV
    