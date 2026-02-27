import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load sounds
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")
powerup_sound = pygame.mixer.Sound("powerup.wav")




# Set up display
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch that - Level 2")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Player setup
player_size = 40
player = pygame.Rect(50, 50, player_size, player_size)
base_speed = 5
player_speed = base_speed

# Walls
walls = [
    pygame.Rect(100, 50, 400, 20),     # Top horizontal
    pygame.Rect(50, 120, 20, 200),    # Left vertical
    pygame.Rect(10, 10, 30, 20),    # Mid horizontal
    pygame.Rect(460, 120, 20, 180),    # Right vertical
    pygame.Rect(100, 300, 380, 20),    # Bottom horizontal
    pygame.Rect(200, 200, 20, 80),     # Center vertical
    pygame.Rect(300, 150, 20, 80),     # Center-right vertical
    pygame.Rect(150, 150, 100, 20),    # Left-center horizontal
    pygame.Rect(350, 250, 100, 20),    # Right-center horizontal
]



# Goal
goal = pygame.Rect(540, 340, 40, 40)

# Enemies
enemy1 = pygame.Rect(500, 50, 40, 40)  # Chaser
enemy2 = pygame.Rect(100, 350, 40, 40)  # Patroller
enemy1_speed = 2
enemy2_speed = 3
enemy2_direction = 1

# Power-ups
speed_boost = pygame.Rect(250, 250, 30, 30)
freeze_enemy = pygame.Rect(400, 80, 30, 30)
speed_active = False
freeze_active = False
speed_timer = 0
freeze_timer = 0

# Fonts
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)
win_text = font.render("ye zinda hai", True, GREEN)
lose_text = font.render("Pakda gaya madarchod", True, RED)

# Timer
start_ticks = pygame.time.get_ticks()
time_limit = 20

# Game loop
clock = pygame.time.Clock()
running = True
won = False
lost = False
while running:
    clock.tick(60)
    current_ticks = pygame.time.get_ticks()
    seconds_passed = (current_ticks - start_ticks) // 1000
    time_left = max(0, time_limit - seconds_passed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not won and not lost:
        # Power-up timers
        if speed_active and current_ticks - speed_timer > 5000:
            player_speed = base_speed
            speed_active = False
        if freeze_active and current_ticks - freeze_timer > 5000:
            freeze_active = False

        # Movement logic
        keys = pygame.key.get_pressed()
        new_position = player.copy()
        if keys[pygame.K_LEFT]:
            new_position.x -= player_speed
        if keys[pygame.K_RIGHT]:
            new_position.x += player_speed
        if keys[pygame.K_UP]:
            new_position.y -= player_speed
        if keys[pygame.K_DOWN]:
            new_position.y += player_speed

        # Collision checks
        collision = any(new_position.colliderect(wall) for wall in walls)
        out_of_bounds = (
            new_position.left < 0 or
            new_position.right > WIDTH or
            new_position.top < 0 or
            new_position.bottom > HEIGHT
        )
        if not collision and not out_of_bounds:
            player = new_position

        # Power-up activation
        if player.colliderect(speed_boost):
            player_speed = base_speed + 3
            speed_active = True
            speed_timer = current_ticks
            speed_boost.x = -100
            powerup_sound.play()



        if player.colliderect(freeze_enemy):
            freeze_active = True
            freeze_timer = current_ticks
            freeze_enemy.x = -100
            powerup_sound.play()

        # Enemy 1: Chaser
        if not freeze_active:
            if enemy1.x < player.x:
                enemy1.x += enemy1_speed
            elif enemy1.x > player.x:
                enemy1.x -= enemy1_speed
            if enemy1.y < player.y:
                enemy1.y += enemy1_speed
            elif enemy1.y > player.y:
                enemy1.y -= enemy1_speed

        # Enemy 2: Patroller
        if not freeze_active:
            enemy2.x += enemy2_speed * enemy2_direction
            if enemy2.left <= 0 or enemy2.right >= WIDTH:
                enemy2_direction *= -1

        # Collision with enemies
        if player.colliderect(enemy1) or player.colliderect(enemy2):
            lost = True
            lose_sound.play()

        # Win condition
        if player.colliderect(goal):
            won = True
            win_sound.play()

        # Time out
        if time_left == 0:
            lost = True
            lose_sound.play()

    # Draw everything
    win.fill(WHITE)
    pygame.draw.rect(win, BLUE, player)
    for wall in walls:
        pygame.draw.rect(win, BLACK, wall)
    pygame.draw.rect(win, GREEN, goal)
    pygame.draw.rect(win, RED, enemy1)
    pygame.draw.rect(win, RED, enemy2)
    pygame.draw.rect(win, YELLOW, speed_boost)
    pygame.draw.rect(win, CYAN, freeze_enemy)

    # Timer display
    timer_text = small_font.render(f"Time Left: {time_left}s", True, RED)
    win.blit(timer_text, (10, 10))

    # Win/Lose messages
    if won:
        win.blit(win_text, (WIDTH // 2 - 120, HEIGHT // 2 - 24))
    elif lost:
        win.blit(lose_text, (WIDTH // 2 - 100, HEIGHT // 2 - 24))

    pygame.display.update()

pygame.quit()
sys.exit()
