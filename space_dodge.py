import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Dodge")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 100, 255)

# Player settings
PLAYER_SIZE = 50
PLAYER_SPEED = 8
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT - PLAYER_SIZE - 20

# Meteor settings
METEOR_SIZE = 40
METEOR_SPEED = 5
meteors = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 800)  # Spawn meteor every 800ms

# Game variables
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)
game_over = False

def draw_player():
    # Draw a simple rocket shape
    pygame.draw.polygon(screen, BLUE, [
        (player_x + PLAYER_SIZE // 2, player_y),  # Top
        (player_x, player_y + PLAYER_SIZE),      # Bottom left
        (player_x + PLAYER_SIZE // 4, player_y + PLAYER_SIZE - 10),  # Inner bottom left
        (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE - 5),   # Inner center
        (player_x + PLAYER_SIZE * 3 // 4, player_y + PLAYER_SIZE - 10),  # Inner bottom right
        (player_x + PLAYER_SIZE, player_y + PLAYER_SIZE),  # Bottom right
    ])

def draw_meteor(x, y):
    # Draw a simple meteor shape
    pygame.draw.circle(screen, GRAY, (x + METEOR_SIZE // 2, y + METEOR_SIZE // 2), METEOR_SIZE // 2)
    pygame.draw.circle(screen, WHITE, (x + METEOR_SIZE // 3, y + METEOR_SIZE // 3), METEOR_SIZE // 6)
    pygame.draw.circle(screen, WHITE, (x + METEOR_SIZE * 2 // 3, y + METEOR_SIZE // 4), METEOR_SIZE // 8)

def check_collision(px, py, psize, mx, my, msize):
    # Check if rectangles overlap
    return (px < mx + msize and px + psize > mx and 
            py < my + msize and py + psize > my)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SPAWN_EVENT and not game_over:
            # Spawn new meteor at random x position at top of screen
            meteor_x = random.randint(0, SCREEN_WIDTH - METEOR_SIZE)
            meteor_y = -METEOR_SIZE
            meteors.append([meteor_x, meteor_y])
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    game_over = False
                    player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
                    player_y = SCREEN_HEIGHT - PLAYER_SIZE - 20
                    meteors.clear()
                    score = 0
                    # Reset difficulty
                    METEOR_SPEED = 5
                    pygame.time.set_timer(SPAWN_EVENT, 800)
    
    if not game_over:
        # Get pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
            player_x += PLAYER_SPEED
        
        # Update meteors
        for meteor in meteors[:]:
            meteor[1] += METEOR_SPEED  # Move meteor down
            
            # Remove meteor if it goes off screen
            if meteor[1] > SCREEN_HEIGHT:
                meteors.remove(meteor)
                score += 1  # Increase score for dodging
            
            # Check collision with player
            elif check_collision(player_x, player_y, PLAYER_SIZE, 
                               meteor[0], meteor[1], METEOR_SIZE):
                game_over = True
        
        # Increase difficulty over time
        if score % 10 == 0 and score > 0:
            METEOR_SPEED = 5 + (score // 10)
            # Adjust spawn rate slightly
            spawn_interval = max(200, 800 - (score // 2) * 10)
            pygame.time.set_timer(SPAWN_EVENT, spawn_interval)
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw player
    draw_player()
    
    # Draw meteors
    for meteor in meteors:
        draw_meteor(meteor[0], meteor[1])
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw game over message
    if game_over:
        game_over_text = font.render("GAME OVER! Press SPACE to restart", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(game_over_text, text_rect)
        
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        screen.blit(final_score_text, score_rect)
    
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()
sys.exit()