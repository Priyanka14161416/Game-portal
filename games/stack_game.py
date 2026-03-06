import pygame
import random

def run_stack():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("Stack Game")
    clock = pygame.time.Clock()
    score = 0
    running = True

    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    score += random.randint(5, 15)

        font = pygame.font.SysFont(None, 40)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (120, 280))

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    return score
