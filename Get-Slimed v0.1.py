import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Get Slimed!")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0) # Placeholder for arena/background
BROWN = (139, 69, 19) # Placeholder for castle
SLIME_GREEN = (0, 150, 0) # Placeholder for slime creatures
RED = (255, 0, 0) # For health bar or game over indication
BLUE = (0, 0, 255) # Player color
YELLOW = (255, 255, 0) # Projectile color

# Castle properties (simplified square)
castle_width = 100
castle_height = 100
castle_x = (SCREEN_WIDTH - castle_width) // 2
castle_y = (SCREEN_HEIGHT - castle_height) // 2
castle_rect = pygame.Rect(castle_x, castle_y, castle_width, castle_height)
castle_health = 100 # Initial castle health
max_castle_health = 100

# Player properties
player_width = 30
player_height = 30
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_speed = 5

# Projectile properties
projectile_size = 10
projectile_speed = 7
projectiles = []

# Slime properties
num_slimes = 10
slime_size = 20
slime_speed = 1 # How fast slimes move
slimes = []
for _ in range(num_slimes):
    slime_x = random.randint(0, SCREEN_WIDTH - slime_size)
    slime_y = random.randint(0, SCREEN_HEIGHT - slime_size)
    slimes.append(pygame.Rect(slime_x, slime_y, slime_size, slime_size))

# Font for displaying text
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire projectile from player's center top
                projectile_x = player_rect.centerx - projectile_size // 2
                projectile_y = player_rect.top - projectile_size
                projectiles.append(pygame.Rect(projectile_x, projectile_y, projectile_size, projectile_size))

    if castle_health <= 0:
        running = False # End game if castle health is zero

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += player_speed

    # Projectile movement
    for projectile in projectiles:
        projectile.y -= projectile_speed
        # Remove projectiles that go off-screen
        if projectile.bottom < 0:
            projectiles.remove(projectile)

    # Slime movement
    for slime in slimes:
        # Calculate direction towards the castle center
        dx = (castle_rect.centerx - slime.centerx)
        dy = (castle_rect.centery - slime.centery)
        dist = (dx**2 + dy**2)**0.5 # Distance formula

        if dist > 0: # Avoid division by zero
            # Normalize direction and multiply by speed
            slime.x += int(slime_speed * (dx / dist))
            slime.y += int(slime_speed * (dy / dist))

    # Collision detection and castle health reduction
    slimes_to_remove = []
    for slime in slimes:
        if castle_rect.colliderect(slime):
            castle_health -= 10 # Reduce health by 10 for each collision
            slimes_to_remove.append(slime)
            if castle_health <= 0:
                castle_health = 0
                break

    # Projectile-slime collision
    projectiles_to_remove = []
    for projectile in projectiles:
        for slime in slimes:
            if projectile.colliderect(slime):
                projectiles_to_remove.append(projectile)
                slimes_to_remove.append(slime)
                break # Only one projectile can hit one slime at a time

    # Remove collided slimes
    for slime in slimes_to_remove:
        if slime in slimes: # Check if slime still exists before removing
            slimes.remove(slime)

    # Remove collided projectiles
    for projectile in projectiles_to_remove:
        if projectile in projectiles: # Check if projectile still exists before removing
            projectiles.remove(projectile)

    # If all slimes are gone, add more (simple wave mechanic)
    if not slimes and castle_health > 0:
        for _ in range(num_slimes):
            slime_x = random.randint(0, SCREEN_WIDTH - slime_size)
            slime_y = random.randint(0, SCREEN_HEIGHT - slime_size)
            slimes.append(pygame.Rect(slime_x, slime_y, slime_size, slime_size))

    # Drawing
    screen.fill(GREEN)  # Arena background

    # Draw castle
    pygame.draw.rect(screen, BROWN, castle_rect)

    # Draw castle health bar (simple)
    health_bar_width = castle_width
    health_bar_height = 10
    health_bar_x = castle_x
    health_bar_y = castle_y - health_bar_height - 5 # Above the castle
    current_health_width = (castle_health / max_castle_health) * health_bar_width

    pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height)) # Background
    pygame.draw.rect(screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_bar_height)) # Current health

    # Draw player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.rect(screen, YELLOW, projectile)

    # Draw slimes
    for slime in slimes:
        pygame.draw.rect(screen, SLIME_GREEN, slime)

    # Display castle health text
    health_text = font.render(f"Castle Health: {castle_health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    # Check for game over condition and display message
    if castle_health <= 0:
        game_over_text = font.render("GAME OVER - Castle Destroyed!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pygame.display.flip() # Update the full display Surface to the screen

    clock.tick(60) # Limit frame rate to 60 FPS

pygame.quit()
print("Pygame window closed.")
