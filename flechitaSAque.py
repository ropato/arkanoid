import pygame
import math


class FlechitaSaque(pygame.sprite.Sprite):
    
    def __init__(self, x, y, length, thickness):
        self.length = length
        self.thickness = thickness
        self.angle = 0

        # Crear una superficie de imagen para la flecha
        self.image = pygame.Surface((length, length), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, rotation_speed,joystick):
        if self.angle <= 89 and self.angle >= -89:
            if joystick[pygame.K_a]:
                self.angle -= rotation_speed  # Reducir el ángulo en sentido contrario a las agujas del reloj
            elif joystick[pygame.K_d]:
                self.angle += rotation_speed  # Aumentar el ángulo en sentido de las agujas del reloj
        else:
            if self.angle > 89:
                self.angle = -89
            else:
                self.angle = 89


    def draw(self, SCR, x, y):
        end_x = x + int(math.sin(math.radians(self.angle)) * self.length)
        end_y = y - int(math.cos(math.radians(self.angle)) * self.length)
        left_x = end_x + int(math.sin(math.radians(self.angle + 150)) * self.thickness)
        left_y = end_y - int(math.cos(math.radians(self.angle + 150)) * self.thickness)
        right_x = end_x + int(math.sin(math.radians(self.angle - 150)) * self.thickness)
        right_y = end_y - int(math.cos(math.radians(self.angle - 150)) * self.thickness)

        self.image.fill((0, 0, 0, 0))  # Rellena la superficie de imagen con transparencia
        # Dibujar la base de la flecha
        pygame.draw.line(SCR, (255, 255, 255), (x, y), (end_x, end_y), 3)

        # Dibujar la parte superior de la flecha
        pygame.draw.polygon(SCR, (255, 255, 255), [(end_x, end_y), (left_x, left_y), (right_x, right_y)])

        SCR.blit(self.image, self.rect)