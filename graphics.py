import pygame
from pygame.locals import *
import pygame.sysfont

class Item():
    def __init__(self, position, color):
        self.position = position
        self.color = color
        
    def move(self, position):
        self.position = position
        
    def set_color(self, color):
        self.color = color
        
    def draw(self, screen):
        print("Uh-oh, child class doesn't implement it's own draw method")

class Text(Item):
    def __init__(self, text="", position=(0,0), fontsize=48, color=(0,0,0)):
        pygame.font.init()
        pygame.font.get_default_font()
        self.font = pygame.font.Font(None, fontsize)
        self.color = color
        self.text = text
        self.position = position
        
    def _render(self):
        return self.font.render(self.text, True, self.color)
    
    def draw(self, screen):
        img = self._render()
        rect = img.get_rect()
        rect.center = self.position
        screen.blit(img, rect)
        
    def set_fontsize(self, fontsize):
        self.font = pygame.font.Font(None, fontsize)
        
    def change_text(self, text):
        self.text = text
        
class Rectangle(Item):
    def __init__(self, position=(0,0), width=10, height=10, color=(0,0,0)):
        super().__init__(position, color)
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0,0, width, height)
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)