from scene_base import Scene_base
from graphics import Rectangle, Text
from game_pieces import Paddle, Ball, Wall
import pygame
from pygame.locals import *
import math

board_color = (0, 0, 0)
player_color = (137, 207, 240)
opponent_color = (248, 131, 121)
ball_color = (170, 255, 0)

board_top = 163
board_bottom = 773
board_left = 27
board_right = 1123
board_centerx = 575
board_centery = 468
board_width = board_right - board_left
board_height = board_bottom - board_top

paddle_width = 10
paddle_height = 68
paddle_player_x = board_left + 20
paddle_opnt_x = board_right - 20
paddle_move_speed = 8

ball_diameter = 16

class Game_scene(Scene_base):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.board = Rectangle((board_centerx, board_centery), board_width, board_height, board_color)
        self.player = Paddle((paddle_player_x, board_centery), paddle_width, paddle_height, player_color, mass=5)
        self.opponent = Paddle((paddle_opnt_x, board_centery), paddle_width, paddle_height, opponent_color, mass=5)
        self.ball = Ball((board_centerx, board_centery), ball_diameter, ball_color, mass=1)
        
        self.player_score = 0
        self.opponent_score = 0
        self.player_moving = False
        self.player_moving_up = False
        self.opponent_moving = False
        self.opponent_moving_up = False
        
        self.max_vel = 8
        self.grav_const = 10
        self.grav_min_dist = 10
        
        self.player_score_label = Text("000", (board_left + board_width//4, board_top - 50))
        self.opponent_score_label = Text("000", (board_centerx + board_width//4, board_top - 50))
        
        self.top_wall = Wall((board_centerx, board_top - 1), board_width, 1)
        self.bottom_wall = Wall((board_centerx, board_bottom), board_width, 1)
        self.left_wall = Wall((board_left - 1, board_centery), 1, board_height)
        self.right_wall = Wall((board_right, board_centery), 1, board_height)
        
    def Process_input(self, events, pressed_keys):
        # Process the W and S keys to move player up/down
        self.player_moving = False
        self.player_moving_up = False
        if pressed_keys[pygame.K_w]:
            self.player_moving = True
            self.player_moving_up = True
            self.player.move((0, -paddle_move_speed))
        elif pressed_keys[pygame.K_s]:
            self.player_moving = True
            self.player.move((0, paddle_move_speed))
                    
        # Determine player collisions with walls
        if self.player.rect.top < board_top:
            self.player_moving = False
            self.player.rect.top = board_top
        if self.player.rect.bottom > board_bottom:
            self.player_moving = False
            self.player.rect.bottom = board_bottom
    
    def Update(self):
        # Move AI Opponent
        self.opponent_moving = False
        self.opponent_moving_up = False
        if self.ball.rect.centerx >= board_left + board_width // 3 * 2:
            if self.opponent.rect.top > self.ball.rect.centery:
                self.opponent_moving = True
                self.opponent_moving_up = True
                self.opponent.move((0, -paddle_move_speed))
            elif self.opponent.rect.bottom < self.ball.rect.centery:
                self.opponent_moving = True
                self.opponent.move((0, paddle_move_speed))
                
        if self.opponent.rect.top < board_top:
            self.opponent_moving = False
            self.opponent.rect.top = board_top
        if self.opponent.rect.bottom > board_bottom:
            self.opponent_moving = False
            self.opponent.rect.bottom = board_bottom
        
        # Update Ball position
        self.ball.move((self.ball.vel_x, self.ball.vel_y))
        
        # Calculate collisions with walls or paddles
        if self.ball.rect.colliderect(self.top_wall) or self.ball.rect.top < board_top:
            self.ball.vel_y = -self.ball.vel_y
            self.ball.rect.top = board_top
            
        if self.ball.rect.colliderect(self.bottom_wall) or self.ball.rect.bottom > board_bottom:
            self.ball.vel_y = -self.ball.vel_y
            self.ball.rect.bottom = board_bottom
            
        if self.ball.rect.colliderect(self.player):
            self.ball.vel_x = -self.ball.vel_x
            self.ball.rect.left = self.player.rect.right
            if self.player_moving:
                temp = -paddle_move_speed if self.player_moving_up else paddle_move_speed
                self.ball.vel_y = (self.ball.mass * self.ball.vel_y + self.player.mass * temp) // (self.ball.mass + self.player.mass)
            
        if self.ball.rect.colliderect(self.opponent):
            self.ball.vel_x = -self.ball.vel_x
            self.ball.rect.right = self.opponent.rect.left
            if self.player_moving:
                temp = -paddle_move_speed if self.opponent_moving_up else paddle_move_speed
                self.ball.vel_y = (self.ball.mass * self.ball.vel_y + self.opponent.mass * temp) // (self.ball.mass + self.opponent.mass)
                
        # Calculate graviational effect on the ball from the paddles
        player_ball_rad_x =  self.player.rect.centerx - self.ball.rect.centerx
        player_ball_rad_y = self.player.rect.centery - self.ball.rect.centery
        player_ball_rad = math.sqrt(player_ball_rad_x**2 + player_ball_rad_y**2)
        f1 = self.grav_const * self.ball.mass * self.player.mass / player_ball_rad
        
        opnt_ball_rad_x = self.opponent.rect.centerx - self.ball.rect.centerx
        opnt_ball_rad_y = self.opponent.rect.centery - self.ball.rect.centery
        opnt_ball_rad = math.sqrt(opnt_ball_rad_x**2 + opnt_ball_rad_y**2)
        f2 = self.grav_const * self.ball.mass * self.opponent.mass / opnt_ball_rad
        
        if opnt_ball_rad > self.grav_min_dist:
            self.ball.vel_x += math.trunc(f2 * opnt_ball_rad_x / opnt_ball_rad)
            self.ball.vel_y += math.trunc(f2 * opnt_ball_rad_y / opnt_ball_rad)

        if player_ball_rad > self.grav_min_dist:
            self.ball.vel_x += math.trunc(f1 * player_ball_rad_x / player_ball_rad)
            self.ball.vel_y += math.trunc(f1 * player_ball_rad_y / player_ball_rad)
        
        # Impose speed limit on ball
        if self.ball.vel_x > self.max_vel:
            self.ball.vel_x = self.max_vel
                
        if self.ball.vel_y > self.max_vel:
            self.ball.vel_y = self.max_vel
            
        # determine if ball hits left or right wall for scoring purposes
        if self.ball.rect.colliderect(self.left_wall) or self.ball.rect.left < board_left:
            self.opponent_score += 1
            if self.opponent_score > 1000:
                self.opponent_score = 0
                
            self.ball.rect.center = (board_centerx, board_centery)
            self.ball.rand_speed()
        
        if self.ball.rect.colliderect(self.right_wall) or self.ball.rect.right > board_right:
            self.player_score += 1
            if self.player_score > 1000:
                self.player_score = 0
                
            self.ball.rect.center = (board_centerx, board_centery)
            self.ball.rand_speed()
        
        # Update Score
        self.player_score_label.change_text(f"{self.player_score:03d}")
        self.opponent_score_label.change_text(f"{self.opponent_score:03d}")
    
    def Render(self, screen):
        screen.fill((127, 127, 127))
        self.board.draw(screen)
        self.player.draw(screen)
        self.opponent.draw(screen)
        self.ball.draw(screen)
        self.player_score_label.draw(screen)
        self.opponent_score_label.draw(screen)
        
    def Terminate(self):
        return super().Terminate()