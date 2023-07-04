import pygame
import misil

Scale_Factor = 1.2

class Jugador(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("resources/messi.png")
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width/2
        self.rect.y = y
        self.INITIAL_WIDTH = self.rect.width
        self.shoot = 0
        
    
    def moveLeft(self,limX):
        if self.rect.left <= limX:
            pass
        else:
            self.rect.x -= 10
        
        
    
    def moveRight(self,limX):
        if self.rect.right >= limX:
            pass
        else:
            self.rect.x += 10

    def getBig(self):
        if not self.rect.width >= self.INITIAL_WIDTH * 2:
            tempX = self.rect.x
            tempY = self.rect.y
            self.image = pygame.transform.scale(self.image, (self.rect.width * Scale_Factor, self.rect.height))
            self.rect = self.image.get_rect(x=tempX, y=tempY)

    def getSmall(self):
        if not self.rect.width<= self.INITIAL_WIDTH / 2:
            tempX = self.rect.x
            tempY = self.rect.y
            self.image = pygame.transform.scale(self.image, (self.rect.width / Scale_Factor, self.rect.height))
            self.rect = self.image.get_rect(x=tempX, y=tempY)

    
    def getShoot(self):
        return self.shoot
    
    def setShoot(self,num):
        self.shoot = num

    


