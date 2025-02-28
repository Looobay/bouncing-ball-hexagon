import pygame
import math
import sys

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.99
HEX_SIZE = 200
BALL_RADIUS = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChatGPT 4o mini (28/02/2025)")
clock = pygame.time.Clock()

# Ball properties
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [5, 0]

# Hexagon rotation
angle = 0
rotation_speed = 1  # degrees per frame

def draw_hexagon(surface, color, center, size, angle):
    points = []
    for i in range(6):
        theta = math.radians(angle + i * 60)
        x = center[0] + size * math.cos(theta)
        y = center[1] + size * math.sin(theta)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points)

def check_collision(ball_pos, ball_vel):
    # Check collision with hexagon walls
    for i in range(6):
        theta = math.radians(i * 60 + angle)
        next_theta = math.radians((i + 1) % 6 * 60 + angle)
        
        # Calculate wall line segment
        wall_start = (WIDTH // 2 + HEX_SIZE * math.cos(theta),
                      HEIGHT // 2 + HEX_SIZE * math.sin(theta))
        wall_end = (WIDTH // 2 + HEX_SIZE * math.cos(next_theta),
                    HEIGHT // 2 + HEX_SIZE * math.sin(next_theta))
        
        # Check for collision with the wall
        if (ball_pos[0] - BALL_RADIUS < wall_start[0] and
            ball_pos[0] + BALL_RADIUS > wall_end[0] and
            ball_pos[1] - BALL_RADIUS < wall_start[1] and
            ball_pos[1] + BALL_RADIUS > wall_end[1]):
            # Reflect the ball's velocity
            ball_vel[0] = -ball_vel[0] * FRICTION
            ball_vel[1] = -ball_vel[1] * FRICTION

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update ball position
    ball_vel[1] += GRAVITY  # Apply gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check for collisions
    check_collision(ball_pos, ball_vel)

    # Rotate the hexagon
    angle += rotation_speed
    if angle >= 360:
        angle -= 360

    # Draw everything
    screen.fill((255, 255, 255))  # Clear screen
    draw_hexagon(screen, (0, 0, 255), (WIDTH // 2, HEIGHT // 2), HEX_SIZE, angle)
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Maintain frame rate