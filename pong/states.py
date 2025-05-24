import pygame
import numpy as np
import copy
from pong.config import WIDTH, HEIGHT, BAR_HEIGHT, BAR_WIDTH, OFFSET, GREEN, BLUE, YELLOW, BLACK, FPS, PURPLE, AQUA, WHITE
from pong.objects import Player, Ball
from pong.utils import mid
from pong.sounds import load_sounds

class Game:
    def __init__(self):
        self.against_computer = True
        pygame.init()
        pygame.display.set_caption("Ping Pong")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.sounds = load_sounds()
        self.running = True
        self.state = "ready"  # can be "ready", "playing", "winner"
        self.setup_players()
        self.start_tick = pygame.time.get_ticks()
        self.winner_player = None
        self.n_rounds = 10

    def setup_players(self):
        self.p1 = Player(
            x=OFFSET,
            y=mid(HEIGHT, BAR_HEIGHT),
            width=BAR_WIDTH,
            height=BAR_HEIGHT//2,
            speed=10, 
            color=GREEN
        )
        self.p2 = Player(
            x=WIDTH - OFFSET - BAR_WIDTH,
            y=mid(HEIGHT, BAR_HEIGHT),
            width=BAR_WIDTH,
            height=BAR_HEIGHT//2,
            speed=10,
            color=BLUE
        )
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, radius=10, speed=6, color=YELLOW)
        if self.against_computer is True:
            self.p1.height *= 0.5

        self.p1_initial = copy.deepcopy(self.p1)
        self.p2_initial = copy.deepcopy(self.p2)
        self.ball_initial = copy.deepcopy(self.ball)

    def run(self):
        while self.running:
            if self.state == "ready":
                self.ready_state()
            elif self.state == "playing":
                self.playing_state()
            elif self.state == "winner":
                self.winner_state()
            self.clock.tick(FPS)

    def ready_state(self):
        self.sounds["get_ready"].play(loops=-1)
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 250)
        ready_text = font.render("READY?!", True, PURPLE)
        ready_text.set_alpha(100)
        self.screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2,
                                      HEIGHT // 2 - ready_text.get_height() // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                for alpha in range(100, -1, -10):
                    ready_text.set_alpha(alpha)
                    self.screen.fill(BLACK)
                    self.screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2,
                                                  HEIGHT // 2 - ready_text.get_height() // 2))
                    pygame.display.flip()
                pygame.mixer.music.play(-1, 5, 5000)
                self.start_tick = pygame.time.get_ticks()
                self.sounds["get_ready"].stop()
                self.state = "playing"

    def playing_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.p2.y_dir = -1
                if event.key == pygame.K_DOWN:
                    self.p2.y_dir = 1
                if event.key == pygame.K_w:
                    self.p1.y_dir = -1
                if event.key == pygame.K_s:
                    self.p1.y_dir = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.p2.y_dir = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    self.p1.y_dir = 0

        if self.ball.ball.colliderect(self.p1.bar):
            self.ball.bounce() 
            self.sounds["ping"].play()
        if self.ball.ball.colliderect(self.p2.bar):
            self.ball.bounce() 
            self.sounds["pong"].play()

        self.p1.update(self.p1.y_dir)
        self.p2.update(self.p2.y_dir)
        if self.against_computer:
            self.p1.auto_move(self.ball)
        self.ball.update_position()        
        point = self.ball.update_score()
        if point:
            self.sounds["loss"].play()
            self.start_tick = pygame.time.get_ticks()            
            self.p1.score += point == -1
            self.p2.score += point == 1
            self.ball.reset()
            if self.against_computer:
                self.p1.speed = self.p1.init_speed
                self.p1.x, self.p1.y  = OFFSET, mid(HEIGHT, BAR_HEIGHT)
                if point == 1:
                    self.p2.height *=0.9 
            else:
                self.p1.height *= 1 - 0.1*(point == -1)
                self.p2.height *= 1 - 0.1*(point == 1) 

        rally_time = pygame.time.get_ticks()-self.start_tick
        increment = 1 + 0.5 * np.log1p(rally_time / 1000)
        self.ball.speed = self.ball.init_speed*increment

        self.screen.fill(BLACK)
        self.p1.show_score(self.screen, WIDTH//4, HEIGHT//2, GREEN)
        self.p2.show_score(self.screen, WIDTH//4*3, HEIGHT//2, BLUE)
        self.p1.display(self.screen)
        self.p2.display(self.screen)
        self.ball.display(self.screen)
        pygame.display.flip()

        if self.p1.score == self.n_rounds or self.p2.score == self.n_rounds:
            self.state = "winner"

    def winner_state(self):

        
        if self.p1.score == self.n_rounds:
            self.p1.winner = True
            self.winner_player = self.p1 
            if self.against_computer:
                self.winner_player.text = "You lose... :("
                self.sounds["loser"].play()
            else:
                self.winner_player.text = "Left player wins!"
                self.sounds["winner"].play(loops=-1)
        if self.p2.score == self.n_rounds:
            self.sounds["winner"].play(loops=-1)
            self.p2.winner = True
            self.winner_player = self.p2
            if self.against_computer:
                self.winner_player.text = "You win! :)"
            else:
                self.winner_player.text = "Right player wins!"
        self.p1 = copy.deepcopy(self.p1_initial)
        self.p2 = copy.deepcopy(self.p2_initial)
        self.ball = copy.deepcopy(self.ball_initial)
        pygame.mixer.music.pause()
        pygame.time.wait(1000)

        # Winner animation setup
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 20, 20
        colors = [BLUE, YELLOW, GREEN, BLUE, PURPLE, GREEN, AQUA, WHITE]
        color_index = 0
        trail = []
        trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        winner = True
        while winner:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    winner = False
                if event.type == pygame.KEYDOWN:
                    winner = False
            self.screen.fill(BLACK)

            if self.winner_player.text != "You lose... :(":
                ball_x += ball_dx
                ball_y += ball_dy
                if ball_x <= 0 or ball_x >= WIDTH:
                    ball_dx *= -1
                if ball_y <= 0 or ball_y >= HEIGHT:
                    ball_dy *= -1
                trail.append((ball_x, ball_y, color_index))
                if len(trail) > 1000:
                    trail.pop(0)
                trail_surface.fill((0, 0, 0, 0))
                for i, (tx, ty, ci) in enumerate(trail):
                    alpha = int(255 * (i + 1) / len(trail) * 0.8)
                    color = colors[ci % len(colors)]
                    pygame.draw.circle(trail_surface, color + (alpha,), (int(tx), int(ty)), 10)
                self.screen.blit(trail_surface, (0, 0))
                color = colors[color_index % len(colors)]
                pygame.draw.circle(self.screen, color, (int(ball_x), int(ball_y)), 10)
                color_index = (color_index + 1) % len(colors)
            font = pygame.font.SysFont(None, 150)
            winner_text = font.render(self.winner_player.text, True, self.winner_player.color)
            text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 180))
            self.screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
            winner_text.set_alpha(300)
            self.screen.blit(winner_text, text_rect)
            pygame.display.flip()
            self.clock.tick(60)
        self.sounds["winner"].stop()
        self.sounds["loser"].stop()
        self.state = "ready"
