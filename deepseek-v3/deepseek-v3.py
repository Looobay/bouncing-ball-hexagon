import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeepSeek v3 (28/02/2025)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0
hexagon_rotation_speed = 0.01

# Ball properties
ball_radius = 20
ball_pos = [WIDTH // 2, HEIGHT // 2 - hexagon_radius + ball_radius]
ball_vel = [random.uniform(-5, 5), 0]
gravity = 0.5
friction = 0.99

# Function to calculate hexagon vertices
def calculate_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        x = center[0] + radius * math.cos(math.radians(60 * i + angle))
        y = center[1] + radius * math.sin(math.radians(60 * i + angle))
        vertices.append((x, y))
    return vertices

# Function to check collision between ball and hexagon walls
def check_collision(ball_pos, ball_radius, hexagon_vertices):
    for i in range(len(hexagon_vertices)):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % len(hexagon_vertices)]
        
        # Calculate the normal vector of the wall
        wall_vector = (p2[0] - p1[0], p2[1] - p1[1])
        normal_vector = (-wall_vector[1], wall_vector[0])
        normal_length = math.hypot(normal_vector[0], normal_vector[1])
        normal_vector = (normal_vector[0] / normal_length, normal_vector[1] / normal_length)
        
        # Calculate the distance from the ball to the wall
        ball_to_wall = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        distance = abs(ball_to_wall[0] * normal_vector[0] + ball_to_wall[1] * normal_vector[1])
        
        if distance < ball_radius:
            # Reflect the ball's velocity
            dot_product = ball_vel[0] * normal_vector[0] + ball_vel[1] * normal_vector[1]
            ball_vel[0] -= 2 * dot_product * normal_vector[0]
            ball_vel[1] -= 2 * dot_product * normal_vector[1]
            return True
    return False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle += hexagon_rotation_speed
    hexagon_vertices = calculate_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_angle)

    # Update ball position and velocity
    ball_vel[1] += gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_vel[0] *= friction
    ball_vel[1] *= friction

    # Check for collisions with hexagon walls
    if check_collision(ball_pos, ball_radius, hexagon_vertices):
        ball_vel[0] *= friction
        ball_vel[1] *= friction

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.polygon(screen, BLACK, hexagon_vertices, 2)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
