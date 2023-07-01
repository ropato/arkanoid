import pygame
SPRITE_SIZE = (50, 50)
class powerUp (pygame.sprite.Sprite):
    def __init__(self,x,y, powerUp,imagen:str):
        super().__init__()
        self.image = pygame.image.load(imagen)
        self.image = pygame.transform.scale(self.image,SPRITE_SIZE)
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.powerUp = powerUp
        self.velocidadV = 3


   
    def fallDown(self):
        self.rect.y+= self.velocidadV