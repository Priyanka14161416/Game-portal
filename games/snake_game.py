import pygame
import random

def run_snake():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake_block = 10
    snake_speed = 15
    x = width / 2
    y = height / 2
    dx = 0
    dy = 0
    snake = []
    length = 1
    score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block; dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block; dy = 0
                elif event.key == pygame.K_UP:
                    dy = -snake_block; dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = snake_block; dx = 0

        x += dx; y += dy
        if x < 0 or x >= width or y < 0 or y >= height:
            running = False

        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), [foodx, foody, 10, 10])

        snake.append([x, y])
        if len(snake) > length: del snake[0]

        for block in snake:
            pygame.draw.rect(screen, (0, 255, 0), [block[0], block[1], 10, 10])

        if x == foodx and y == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1
            score += 10

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    return score
