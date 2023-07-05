import pygame
import powerup
BRICK_SIZE = [70, 20]
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0,0,255)
PURPLE=(148,0,211)



class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,image,posX,posY,resistance, points):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.resistance = resistance
        self.points = points
        self.breakSound = pygame.mixer.Sound("resources/romperLadrillo.mp3")
        
    def getAnchoLadrillo(self):
        return self.rect.width
    
    def getResistance(self):
        return self.resistance
    
    def setResistance(self,resistance):
        self.resistance = resistance

    
class ladrillo_p(Ladrillo):
    def __init__(self, color, posX, posY, resistance, points, powerUp,imgPU):
        super().__init__(color, posX, posY, resistance, points)
        self.powerUp=powerUp
        self.imagenPU = imgPU

    
class normalBrick(Ladrillo):
    def __init__(self, color, posX, posY, resistance, points):
        super().__init__(color, posX, posY, resistance, points)

    def resistanceColor(self):
        if self.resistance == 1:
            self.image = pygame.image.load("resources/ladrilloRojo.png")
        elif self.resistance == 2:
            self.image = pygame.image.load("resources/ladrilloVerde.png")
        elif self.resistance == 3:
            self.image = pygame.image.load("resources/ladrilloAzul.png")

class fallingBrick(Ladrillo):
    def __init__(self, color, posX, posY, resistance, points):
        super().__init__(color, posX, posY, resistance, points)
        self.verticalSpeed = 3
        self.falling = False

    def fall(self):
        self.rect.y += self.verticalSpeed

    def setFalling(self,bool:bool):
        self.falling = bool