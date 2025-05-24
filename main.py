import pygame
from pong.config import WIDTH, HEIGHT, BAR_HEIGHT, BAR_WIDTH, OFFSET, GREEN, BLUE, YELLOW, BLACK, FPS, PURPLE, AQUA, WHITE
from pong.objects import Player, Ball
from pong.utils import mid
from pong.sounds import load_sounds
import numpy as np
import random
import copy


def main():
    ####### SETUP ######
    against_computer = True

    pygame.init()
    pygame.display.set_caption("Ping Pong")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    clock = pygame.time.Clock()  
    sounds = load_sounds()

    p1 = Player(
        x=OFFSET,
        y=mid(HEIGHT, BAR_HEIGHT),
        width=BAR_WIDTH,
        height=BAR_HEIGHT//2,
        speed=10, 
        color=GREEN
    )
    p2 = Player(
        x=WIDTH - OFFSET - BAR_WIDTH,
        y=mid(HEIGHT, BAR_HEIGHT),
        width=BAR_WIDTH,
        height=BAR_HEIGHT//2,
        speed=10,
        color=BLUE
    )
    ball = Ball(WIDTH // 2, HEIGHT // 2, radius=10, speed=6, color=YELLOW)

    p1_initial = copy.deepcopy(p1)
    p2_initial = copy.deepcopy(p2)
    ball_initial = copy.deepcopy(ball)

    if against_computer is True:
        p1.height *= 0.5

    ###### GAME EVENTS ######
    get_ready = True
    running = True
    while running:

        while get_ready is True:
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 250)
            ready_text = font.render("READY?!", True, PURPLE)
            ready_text.set_alpha(100)
            screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2,
                                    HEIGHT // 2 - ready_text.get_height() // 2))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    for alpha in range(100, -1, -10):
                        ready_text.set_alpha(alpha)
                        screen.fill(BLACK)
                        screen.blit(ready_text, (WIDTH // 2 - ready_text.get_width() // 2,
                                                HEIGHT // 2 - ready_text.get_height() // 2))
                        pygame.display.flip()

                    pygame.mixer.music.play(-1, 5, 5000)
                    start_tick = pygame.time.get_ticks()
                    get_ready = False
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    p2.y_dir = -1
                if event.key == pygame.K_DOWN:
                    p2.y_dir = 1
                if event.key == pygame.K_w:
                    p1.y_dir = -1
                if event.key == pygame.K_s:
                    p1.y_dir = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    p2.y_dir = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    p1.y_dir = 0

        if ball.ball.colliderect(p1.bar):
            ball.bounce() 
            sounds["ping"].play()

        if ball.ball.colliderect(p2.bar):
            ball.bounce() 
            sounds["pong"].play()

        ###### UPDATE ######
        p1.update(p1.y_dir)
        p2.update(p2.y_dir)

        if against_computer is True:
            p1.auto_move(ball) # follow ball

        ball.update_position()        
        point = ball.update_score()
        if point:
            sounds["loss"].play()
            start_tick = pygame.time.get_ticks()            
            p1.score += point == -1
            p2.score += point == 1

            ball.reset()
            if against_computer is True:
                p1.speed = p1.init_speed
                p1.x, p1.y  = OFFSET, mid(HEIGHT, BAR_HEIGHT) # reset bar
                if point == 1: # player scores
                    p2.height *=0.9 
            else:
                p1.height *= 1 - 0.1*(point == -1)
                p2.height *= 1 - 0.1*(point == 1) 

        rally_time = pygame.time.get_ticks()-start_tick
        increment = 1 + 0.5 * np.log1p(rally_time / 1000)
        ball.speed = ball.init_speed*increment

        ###### DISPLAY #####
        screen.fill(BLACK)
        p1.show_score(screen, WIDTH//4, HEIGHT//2, GREEN)
        p2.show_score(screen, WIDTH//4*3, HEIGHT//2, BLUE)
        p1.display(screen)
        p2.display(screen)
        ball.display(screen)
        pygame.display.flip()

        ###### WINNER #####
        n_rounds = 1
        if p1.score == n_rounds or p2.score == n_rounds:
            if p1.score == n_rounds:
                p1.winner = True
                winning_player = p1 
                if against_computer is True:
                    winning_player.text = "You lose! :("
                else:
                    winning_player.text = "Left player wins!"
            if p2.score == n_rounds:
                p2.winner = True
                winning_player = p2
                if against_computer is True:
                    winning_player.text = "You win! :)"
                else:
                    winning_player.text = "Right player wins!"

            p1 = copy.deepcopy(p1_initial)
            p2 = copy.deepcopy(p2_initial)
            ball = copy.deepcopy(ball_initial)
            get_ready = True
            winner = True
            pygame.mixer.music.pause()
            pygame.time.wait(1000)

            # Ball animation setup
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx, ball_dy = 20, 20
            colors = [
                BLUE,
                YELLOW,             
                GREEN,              
                BLUE,             
                PURPLE,
                GREEN,             
                AQUA,              
                WHITE
            ]

            color_index = 0
            trail = []

            # Create a transparent surface for the trail
            trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            while winner is True:
                winner_start_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        winner = False
                
                screen.fill(BLACK)
                if winning_player.text == "You lose! :(":
                    # create bouncing rainbow ball
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
                        alpha = int(255 * (i + 1) / len(trail) * 0.8)  # 0.5 for half transparency
                        color = colors[ci % len(colors)]
                        pygame.draw.circle(trail_surface, color + (alpha,), (int(tx), int(ty)), 10)

                    screen.blit(trail_surface, (0, 0))
                    color = colors[color_index % len(colors)]
                    pygame.draw.circle(screen, color, (int(ball_x), int(ball_y)), 10)
                    color_index = (color_index + 1) % len(colors)

                # Draw WINNER text
                font = pygame.font.SysFont(None, 150)
                winner_text = font.render(winning_player.text, True, winning_player.color)
                text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                bg_surface = pygame.Surface((text_rect.width + 40, text_rect.height + 20), pygame.SRCALPHA)
                bg_surface.fill((0, 0, 0, 180))
                screen.blit(bg_surface, (text_rect.x - 20, text_rect.y - 10))
                winner_text.set_alpha(300)
                screen.blit(winner_text, text_rect)

                pygame.display.flip()
                clock.tick(60)


        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()