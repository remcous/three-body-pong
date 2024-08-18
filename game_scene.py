from scene_base import Scene_base
from graphics import Rectangle, Text
from game_pieces import Paddle, Ball, Wall, ProgressBar
import pygame
from pygame.locals import *
import math
import datetime

board_color = (0, 0, 0)
player_color = (137, 207, 240)
player_attack_color = (0, 216, 255)
opponent_color = (248, 131, 121)
opponent_attack_color = (255, 0, 0)
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
        
        self.attack_duration = datetime.timedelta(seconds=1)
        self.attack_cooldown = datetime.timedelta(seconds=8)
        
        self.player_attacking = False
        self.player_attack_start_time = datetime.datetime.now()
        self.player_attack_end_time = datetime.datetime.now() + datetime.timedelta(microseconds=1)
        self.player_attack_cooldown_end = datetime.datetime.now() + datetime.timedelta(microseconds=1)
        self.player_attack_bar = ProgressBar((board_left+100, board_top - 30), 200, 25, player_color, player_attack_color)
        
        self.opnt_attacking = False
        self.opnt_attack_start_time = datetime.datetime.now()
        self.opnt_attack_end_time = datetime.datetime.now() + datetime.timedelta(microseconds=1)
        self.opnt_attack_cooldown_end = datetime.datetime.now() + datetime.timedelta(microseconds=1)
        self.opnt_attack_bar = ProgressBar((board_right-100, board_top - 30), 200, 25, opponent_color, opponent_attack_color)
        
        self.opnt_attack_dist = 8
        self.max_vel = 12
        self.grav_const = 10
        self.grav_min_dist = 2
        
        self.title_label = Text("THREE-BODY PONG", (board_centerx, 40), 60)
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
        if pressed_keys[pygame.K_s]:
            self.player_moving = True
            self.player.move((0, paddle_move_speed))
        if pressed_keys[pygame.K_SPACE]:
            if not self.player_attacking and datetime.datetime.now() > self.player_attack_cooldown_end:
                self.player_attacking = True
                self.player_attack_bar.update_progress(0)
                self.player.mass = -1 * abs(self.player.mass)
                self.player.color = player_attack_color
                self.player_attack_start_time = datetime.datetime.now()
                self.player_attack_end_time = self.player_attack_start_time + self.attack_duration
                self.player_attack_cooldown_end = self.player_attack_start_time + self.attack_cooldown
                    
        # Determine player collisions with walls
        if self.player.rect.top < board_top:
            self.player_moving = False
            self.player.rect.top = board_top
        if self.player.rect.bottom > board_bottom:
            self.player_moving = False
            self.player.rect.bottom = board_bottom
    
    def Update(self):
        current_time = datetime.datetime.now()
            
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
            
        # Handle opponent attack
        if current_time > self.opnt_attack_cooldown_end and abs(self.ball.rect.right - self.opponent.rect.left) < self.opnt_attack_dist:
            self.opnt_attacking = True
            self.opponent.color = opponent_attack_color
            self.opponent.mass = -1 * abs(self.opponent.mass)
            self.opnt_attack_start_time = current_time
            self.opnt_attack_cooldown_end = current_time + self.attack_cooldown
            self.opnt_attack_end_time = current_time + self.attack_duration
            self.opnt_attack_bar.update_progress(0)
        
        if current_time < self.opnt_attack_cooldown_end:
            progress = (current_time - self.opnt_attack_start_time) / (self.opnt_attack_cooldown_end - self.opnt_attack_start_time) * 100
            self.opnt_attack_bar.update_progress(
                progress
            )
        else:
            self.opnt_attack_bar.update_progress(100)
                
        if self.opnt_attacking:
            if current_time >= self.opnt_attack_end_time:
                self.opnt_attacking = False
                self.opponent.color = opponent_color
                self.opponent.mass = abs(self.opponent.mass)
                
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
            # if self.player_moving:
            #     temp = -paddle_move_speed if self.player_moving_up else paddle_move_speed
            #     self.ball.vel_y = (self.ball.mass * self.ball.vel_y + self.player.mass * temp) // (self.ball.mass + self.player.mass)
            
        if self.ball.rect.colliderect(self.opponent):
            self.ball.vel_x = -self.ball.vel_x
            self.ball.rect.right = self.opponent.rect.left
            # if self.player_moving:
            #     temp = -paddle_move_speed if self.opponent_moving_up else paddle_move_speed
            #     self.ball.vel_y = (self.ball.mass * self.ball.vel_y + self.opponent.mass * temp) // (self.ball.mass + self.opponent.mass)
                
        # Handle player attack
        if self.player_attacking:
            if current_time >= self.player_attack_end_time:
                self.player_attacking = False
                self.player.color = player_color
                self.player.mass = abs(self.player.mass)
                
        if current_time < self.player_attack_cooldown_end:
            progress = (current_time - self.player_attack_start_time) / (self.player_attack_cooldown_end - self.player_attack_start_time) * 100
            self.player_attack_bar.update_progress(
                progress
            )
        else:
            self.player_attack_bar.update_progress(100)
                
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
                
            self.player_attack_cooldown_end = current_time
            self.player_attacking = False
            self.player.color = player_color

            self.opnt_attack_cooldown_end = current_time
            self.opnt_attacking = False
            self.opponent.color = opponent_color
            self.ball.rect.center = (board_centerx, board_centery)
            self.ball.rand_speed()
        
        if self.ball.rect.colliderect(self.right_wall) or self.ball.rect.right > board_right:
            self.player_score += 1
            if self.player_score > 1000:
                self.player_score = 0
                
            self.player_attack_cooldown_end = current_time
            self.player_attacking = False
            self.player.color = player_color

            self.opnt_attack_cooldown_end = current_time
            self.opnt_attacking = False
            self.opponent.color = opponent_color
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
        self.title_label.draw(screen)
        self.player_attack_bar.draw(screen)
        self.opnt_attack_bar.draw(screen)
        
    def Terminate(self):
        return super().Terminate()