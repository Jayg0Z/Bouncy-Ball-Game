import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 1200, 800
BALL_RADIUS = 30
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 15
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jayz Bouncy Little Balls!")
font = pygame.font.Font(None, 40)

# Load the background image
background_image = pygame.image.load("football_pitch_3.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Clock to control the frame rate
clock = pygame.time.Clock()

# Load the ball image
ball_image = pygame.image.load("football.png")
ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

# Initialize variables for the game
ball_pos = [WIDTH // 2, HEIGHT // 2]
platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]
platform_speed = 10
score = 0
lives = 3
initial_speed = 3
ball_speed_increment = 1
current_level = 1
ball_speed = [initial_speed, initial_speed]
platform_color = ORANGE  # Initialize platform color

# Functions for screens
def start_screen():
    show_text_on_screen("Jayz Bouncy Little Balls!", 50, HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 30, HEIGHT // 3)
    show_text_on_screen("Move the platform with arrow keys...", 30, HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

def game_over_screen():
    show_text_on_screen("Game Over", 50, HEIGHT // 3)
    show_text_on_screen(f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def victory_screen():
    show_text_on_screen("Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(f"You've won with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to exit...", 20, HEIGHT * 2 // 3)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_text_on_screen(text, font_size, y_position):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, WHITE)
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    screen.blit(text_render, text_rect)

def change_platform_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Main game loop
start_screen()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()
    
    # Clear the screen and draw the background image
    screen.blit(background_image, (0, 0))

    # Move the platform
    platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed
    platform_pos[1] += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * platform_speed

    # Ensure the platform stays within the screen boundaries
    platform_pos[0] = max(0, min(platform_pos[0], WIDTH - PLATFORM_WIDTH))
    platform_pos[1] = max(0, min(platform_pos[1], HEIGHT - PLATFORM_HEIGHT))

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce off the walls
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
        ball_speed[0] = -ball_speed[0]

    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]

    # Check if the ball hits the platform
    if (
        platform_pos[0] <= ball_pos[0] + BALL_RADIUS <= platform_pos[0] + PLATFORM_WIDTH
        and platform_pos[1] <= ball_pos[1] + BALL_RADIUS <= platform_pos[1] + PLATFORM_HEIGHT
    ) or (
        platform_pos[0] <= ball_pos[0] - BALL_RADIUS <= platform_pos[0] + PLATFORM_WIDTH
        and platform_pos[1] <= ball_pos[1] - BALL_RADIUS <= platform_pos[1] + PLATFORM_HEIGHT
    ) or (
        platform_pos[0] <= ball_pos[0] + BALL_RADIUS <= platform_pos[0] + PLATFORM_WIDTH
        and platform_pos[1] <= ball_pos[1] - BALL_RADIUS <= platform_pos[1] + PLATFORM_HEIGHT
    ) or (
        platform_pos[0] <= ball_pos[0] - BALL_RADIUS <= platform_pos[0] + PLATFORM_WIDTH
        and platform_pos[1] <= ball_pos[1] + BALL_RADIUS <= platform_pos[1] + PLATFORM_HEIGHT
    ):
        ball_speed[1] = -ball_speed[1]
        score += 1


    # Check if the player advances to the next level
    if score >= current_level * 5:
        current_level += 1
        ball_speed_increment += 3
        platform_color = change_platform_color()

    # Check if the ball falls off the screen
    if ball_pos[1] >= HEIGHT:
        # Decrease lives
        lives -= 1
        if lives == 0:
            game_over_screen()
            start_screen()  # Restart the game after game over
            score = 0
            lives = 3
            current_level = 1
        else:
            # Reset the ball position
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            # Randomize the ball speed
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]

    # Draw the ball image
    screen.blit(ball_image, (int(ball_pos[0] - BALL_RADIUS), int(ball_pos[1] - BALL_RADIUS)))

    # Draw the platform with a white border
    pygame.draw.rect(screen, WHITE, (int(platform_pos[0]) - 2, int(platform_pos[1]) - 2, PLATFORM_WIDTH + 4, PLATFORM_HEIGHT + 4))
    pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]), PLATFORM_WIDTH, PLATFORM_HEIGHT))


    # Display information
    info_line_y = 10  # Adjust the vertical position as needed
    info_spacing = 75  # Adjust the spacing as needed

    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top center
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(center=(WIDTH // 2, info_line_y + 12))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the lives in a red rectangle at the top right
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    lives_rect = lives_text.get_rect(topright=(WIDTH - 10, info_line_y))
    pygame.draw.rect(screen, RED, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()