import pygame

Scale_Factor = 1.2
class Jugador(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("jugador.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def izquierda(self,limX):
        if self.rect.left <= limX:
            pass
        else:
            self.rect.x -= 10
        
        
    
    def derecha(self,limX):
        if self.rect.right >= limX:
            pass
        else:
            self.rect.x += 10

    def getBig(self):
        tempX = self.rect.x
        tempY = self.rect.y
        self.image = pygame.transform.scale(self.image, (self.rect.width * Scale_Factor, self.rect.height))
        self.rect = self.image.get_rect(x=tempX, y=tempY)
