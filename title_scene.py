from scene_base import Scene_base
from game_scene import Game_scene
from graphics import Text
import pygame
from pygame.locals import *

class Title_scene(Scene_base):
    def __init__(self):
        Scene_base.__init__(self)
        self.items = []
        
        self.items.append(Text("THREE-BODY PONG", (575, 300), 80))
        self.items.append(Text("Press ENTER to continue", (575, 400)))
        self.items.append(Text("Press ESC to exit", (575, 450)))
        
    def Process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user preses Enter
                self.Switch_to_scene(Game_scene())
                
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((175, 175, 175))
        for item in self.items:
            item.draw(screen)