from scene_base import Scene_base
import pygame
from pygame.locals import *

class Game_scene(Scene_base):
    def __init__(self):
        super().__init__()
        
    def Process_input(self, events, pressed_keys):
        pass
    
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((127, 127, 127))
        
    def Terminate(self):
        return super().Terminate()