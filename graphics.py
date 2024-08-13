import pygame
from pygame.locals import *
import pygame.sysfont

class Text():
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
        
    def move(self, position):
        self.position = position
        
    def set_fontsize(self, fontsize):
        self.font = pygame.font.Font(None, fontsize)
        
    def set_color(self, color):
        self.color = color
        
    def change_text(self, text):
        self.text = text