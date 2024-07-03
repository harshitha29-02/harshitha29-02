import pygame
import sys
import time
import random

# Game setup
pygame.init()

# Window size
frame_size_x = 720
frame_size_y = 480

# Initialize game window
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Eater')

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Snake and food
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True

# Obstacles
obstacle_pos = [[200, 200], [300, 300], [400, 100]]  # Obstacle positions
obstacle_size = 8

# Game variables
direction = 'RIGHT'
change_to = direction
score = 0
game_over = False

# Game settings
difficulty = 13
fps_controller = pygame.time.Clock()

# Functions
def show_game_over_screen():
    game_window.fill(black)
    font = pygame.font.SysFont('Arial', 50)
    text = font.render('GAME OVER', True, red)
    text_rect = text.get_rect(center=(frame_size_x / 2, frame_size_y / 2 - 50))
    game_window.blit(text, text_rect)
    score_text = font.render(f'Score: {score}', True, white)
    score_rect = score_text.get_rect(center=(frame_size_x / 2, frame_size_y / 2))
    game_window.blit(score_text, score_rect)
    pygame.display.update()
    time.sleep(3)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    # Check collision with obstacles
    for obs in obstacle_pos:
        if snake_pos[0] == obs[0] and snake_pos[1] == obs[1]:
            direction = 'STOP'
            break

    # Game over conditions (when the snake goes out of screen)
    if snake_pos[0] < 0 or snake_pos[0] >= frame_size_x or snake_pos[1] < 0 or snake_pos[1] >= frame_size_y:
        game_over = True

    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True

    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    for obs in obstacle_pos:
        pygame.draw.rect(game_window, blue, pygame.Rect(obs[0], obs[1], obstacle_size, obstacle_size))

    font = pygame.font.SysFont('Arial', 20)
    score_text = font.render(f'Score: {score}', True, white)
    game_window.blit(score_text, (10, 10))

    if direction == 'STOP':
        stop_text = font.render('Hit obstacle! Change direction to continue', True, white)
        game_window.blit(stop_text, (frame_size_x // 2 - 200, frame_size_y // 2))
        pygame.display.update()
        while direction == 'STOP':
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'
                    direction = change_to  # Change direction to continue the game

    pygame.display.update()
    fps_controller.tick(difficulty)

show_game_over_screen()
pygame.quit()
sys.exit()
