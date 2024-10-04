import pygame
import random

# Initialize Pygame
pygame.init()

# Set display dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (0, 0, 255)

# Load images
player_img = pygame.Surface((50, 50))
player_img.fill(green)
enemy1_img = pygame.Surface((50, 50))
enemy1_img.fill(red)
enemy2_img = pygame.Surface((50, 50))
enemy2_img.fill(blue)
bullet_img = pygame.Surface((5, 10))
bullet_img.fill(white)

# Player settings
player_x = width // 2
player_y = height - 70
player_speed = 7

# Bullet settings
bullets = []
bullet_speed = 10

# Enemy settings
enemies = []
enemy_speed = 2

# Game variables
running = True
score = 0
font = pygame.font.SysFont(None, 36)

def create_enemy():
    enemy_type = random.choice(['type1', 'type2'])
    x = random.randint(0, width - 50)
    if enemy_type == 'type1':
        enemies.append([x, 0, enemy1_img, 1])  # (x, y, image, score)
    else:
        enemies.append([x, 0, enemy2_img, 2])  # Different enemy type with different score

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # Player movement
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < width - 50:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit the number of bullets
            bullets.append([player_x + 22, player_y])  # Position bullet on the player's ship

    # Move bullets
    bullets = [[x, y - bullet_speed] for x, y in bullets if y > 0]

    # Create enemies
    if random.randint(1, 40) == 1:  # Randomly create enemies
        create_enemy()

    # Move enemies
    enemies = [[x, y + enemy_speed, img, score] for x, y, img, score in enemies if y < height]

    # Check for collisions
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], 50, 50)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += enemy[3]  # Increase score based on enemy type
                break

    # Fill the screen with black
    screen.fill(black)

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    # Draw bullets
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy[2], (enemy[0], enemy[1]))  # Draw enemy with its respective image

    # Render score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
