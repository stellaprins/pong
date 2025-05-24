import pygame
import random
from pong.config import HEIGHT, WIDTH, font_path
import numpy as np


class Player:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.y_dir = 0
        self.width = width
        self.height = height
        self.speed = speed
        self.init_speed = self.speed
        self.switch_speed = False
        self.color = color
        self.bar = pygame.Rect(x, y, width, height)
        self.dir = 0
        self.score = 0
        self.winner = False
        self.font = font_path()
    
    def display(self,screen):
        self.draw_bar = pygame.draw.rect(screen, self.color, self.bar)

    def update(self, y_dir):
        self.y += self.speed*y_dir
        if self.y <= 0:
            self.y = 0
        elif self.y + self.height >= HEIGHT:
            self.y = HEIGHT-self.height
        self.bar = (self.x, self.y, self.width, self.height)

    def show_score(self, screen, x, y, color, size=200, alpha=80):
        font = pygame.font.Font(self.font, size)
        text = font.render(str(self.score), True, color)
        text.set_alpha(alpha)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)


    def show_winning_score(self, screen, x, y, color, size=350, alpha=255):
        if self.winner:
            duration = 2000  # ms to reach center
            elapsed = min(pygame.time.get_ticks(), duration)
            t = elapsed / duration
            end_x, end_y = WIDTH // 2, HEIGHT // 2
            interp_x = int(x + (end_x - x) * t)
            interp_y = int(y + (end_y - y) * t)
            font = pygame.font.Font(self.font, size)
            text = font.render(str(self.score), True, color)
            text.set_alpha(alpha)
            text_rect = text.get_rect()
            text_rect.center = (interp_x, interp_y)
            screen.blit(text, text_rect)


    def getRect(self):
        return self.bar
    
    def auto_move(self, ball):
        bar_middle = self.y + self.height // 2
        self.follow_ball(ball, bar_middle)
        self.reset_switch_speed(ball)
        self.performance_variation(ball)

    def follow_ball(self, ball, bar_middle):
        """For automove"""
        if ball.x < WIDTH//2 and ball.x_dir < 0:
            if ball.y < bar_middle:
                self.update(-1)
            elif ball.y > bar_middle:
                self.update(1)
            else:
                self.update(0)

    def reset_switch_speed(self, ball):
        """For automove"""
        if ball.x > WIDTH//2 and ball.x_dir < 1:
            self.switch_speed = False

    def performance_variation(self, ball):
        """For automove"""
        if ball.x < WIDTH//2 and ball.x_dir < 0 and self.switch_speed is False:
            variation = 1 + np.random.normal(0.2, 0.2)
            self.speed = self.init_speed * variation
            self.switch_speed = True
            
class Ball:
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.x_dir = 1
        self.y_dir = -1
        self.radius = radius
        self.diameter = self.radius * 2
        self.speed = speed
        self.init_speed = speed
        self.max_speed = self.speed*2
        self.color = color
        self.ball = pygame.Rect(self.x - self.radius, 
                                self.y - self.radius,
                                self.diameter, 
                                self.diameter)
        self.point_awarded = False

    def display(self,screen):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.x, self.y), self.radius)

    def update_position(self):
        self.x += self.speed * self.x_dir
        self.y += self.speed * self.y_dir
        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.y_dir *= -1

    def update_score(self):
        if self.x + self.radius >= WIDTH and not self.point_awarded:
            self.point_awarded = True   
            return -1  # p1 scores
        elif self.x - self.radius <= 0 and not self.point_awarded:
            self.point_awarded = True
            return 1  # p2 scores
        else:
            return 0  # keep 0        

    def reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.x_dir = random.choice((-1, 1))
        self.y_dir = random.choice((-1, 1))
        self.point_awarded = 0
        self.speed = self.init_speed 

    def bounce(self):
        self.x_dir *= -1 

    def getRect(self):
        return self.ball