import pygame
from pygame.locals import *
import random

class GamePiece():
    def __init__(self, position, width, height, color, mass):
        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self.mass = mass
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]
        
    def draw(self, screen):
        print("Uh-oh, you didn't define how the child class should draw itself")
        
    def move(self, position):
        self.rect.move_ip(position[0], position[1])
        
class Paddle(GamePiece):
    def __init__(self, position, width, height, color, mass=0):
        super().__init__(position, width, height, color, mass)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
class Ball(GamePiece):
    def __init__(self, position, diameter, color, mass=0):
        super().__init__(position, diameter, diameter, color, mass)
        self.vel_x = 0
        self.vel_y = 0
        self.rand_speed()
        
    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
        
    def rand_speed(self):
        self.vel_x = random.randint(2, 10)
        if random.randint(0, 1) == 0:
            self.vel_x = -self.vel_x
            
        self.vel_y = random.randint(-10, 10)
        
class Wall(GamePiece):
    def __init__(self, position, width, height):
        super().__init__(position, width, height, None, 0)
        
    def draw(self, screen):
        pass