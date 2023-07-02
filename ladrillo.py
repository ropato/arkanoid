import pygame
import powerup
BRICK_SIZE = [70, 20]
class Ladrillo(pygame.sprite.Sprite):
    def __init__(self,color,posX,posY,resistance, points):
        super().__init__()
        self.image = pygame.Surface(BRICK_SIZE)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = posY
        self.resistance = resistance
        self.points = points
        
    def getAnchoLadrillo(self):
        return self.rect.width

    
class ladrillo_p(Ladrillo):
    def __init__(self, color, posX, posY, resistance, points, powerUp,imgPU):
        super().__init__(color, posX, posY, resistance, points)
        self.powerUp=powerUp
        self.imagenPU = imgPU

    

        