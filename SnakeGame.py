import pygame
import random

# Initialize Pygame
pygame.init()
W, H = 600, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game with Portals")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Game variables
cell_size = 20
snake = [[W//2, H//2]]
direction = [cell_size, 0]
food = [random.randrange(0, W, cell_size), random.randrange(0, H, cell_size)]
portals = [[100, 100], [500, 500]]  # Portal positions
score = 0
game_over = False

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction[1] == 0:
                direction = [0, -cell_size]
            if event.key == pygame.K_DOWN and direction[1] == 0:
                direction = [0, cell_size]
            if event.key == pygame.K_LEFT and direction[0] == 0:
                direction = [-cell_size, 0]
            if event.key == pygame.K_RIGHT and direction[0] == 0:
                direction = [cell_size, 0]
            if event.key == pygame.K_r and game_over:
                snake = [[W//2, H//2]]
                direction = [cell_size, 0]
                food = [random.randrange(0, W, cell_size), random.randrange(0, H, cell_size)]
                score = 0
                game_over = False
    
    if not game_over:
        # Move snake
        head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
        
        # Check for portal teleportation
        if head[0] == portals[0][0] and head[1] == portals[0][1]:
            head = [portals[1][0], portals[1][1]]
        elif head[0] == portals[1][0] and head[1] == portals[1][1]:
            head = [portals[0][0], portals[0][1]]
        
        snake.insert(0, head)
        
        # Check for food collision
        if head[0] == food[0] and head[1] == food[1]:
            food = [random.randrange(0, W, cell_size), random.randrange(0, H, cell_size)]
            score += 1
            # Move portals when food is eaten
            portals[0] = [random.randrange(0, W, cell_size), random.randrange(0, H, cell_size)]
            portals[1] = [random.randrange(0, W, cell_size), random.randrange(0, H, cell_size)]
        else:
            snake.pop()
        
        # Check for game over conditions
        if (head[0] < 0 or head[0] >= W or head[1] < 0 or head[1] >= H or 
            head in snake[1:]):
            game_over = True
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw portals
    pygame.draw.rect(screen, BLUE, (portals[0][0], portals[0][1], cell_size, cell_size))
    pygame.draw.rect(screen, ORANGE, (portals[1][0], portals[1][1], cell_size, cell_size))
    
    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], cell_size, cell_size))
    
    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], cell_size, cell_size))
    
    # Draw score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Game over message
    if game_over:
        font = pygame.font.SysFont(None, 72)
        game_over_text = font.render("GAME OVER", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(game_over_text, (W//2 - 150, H//2 - 50))
        screen.blit(restart_text, (W//2 - 180, H//2 + 20))
    
    pygame.display.flip()
    clock.tick(10)

pygame.quit()