import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChatGPT 4o (28/02/2025)")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Ball properties
ball_radius = 10
ball_pos = [WIDTH // 2, HEIGHT // 4]
ball_vel = [random.uniform(-2, 2), 0]  # Initial velocity
gravity = 0.5
friction = 0.98

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0  # Initial rotation angle
hexagon_rotation_speed = 1  # Degrees per frame

def rotate_point(point, angle, center):
    """Rotate a point around a center by a given angle."""
    x, y = point
    cx, cy = center
    radians = math.radians(angle)
    x -= cx
    y -= cy
    new_x = x * math.cos(radians) - y * math.sin(radians)
    new_y = x * math.sin(radians) + y * math.cos(radians)
    return new_x + cx, new_y + cy

def get_hexagon_points(center, radius, angle):
    """Get the vertices of a hexagon given its center, radius, and rotation angle."""
    points = []
    for i in range(6):
        theta = math.radians(i * 60) + math.radians(angle)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    return points

def reflect_velocity(velocity, normal):
    """Reflect a velocity vector off a surface with a given normal."""
    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
    reflected = [
        velocity[0] - 2 * dot_product * normal[0],
        velocity[1] - 2 * dot_product * normal[1],
    ]
    return reflected

def normalize(vector):
    """Normalize a 2D vector."""
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if length == 0:
        return [0, 0]
    return [vector[0] / length, vector[1] / length]

# Main game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle += hexagon_rotation_speed
    hexagon_points = get_hexagon_points(hexagon_center, hexagon_radius, hexagon_angle)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon_points, 2)

    # Update ball position
    ball_vel[1] += gravity  # Apply gravity
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check for collisions with hexagon walls
    for i in range(6):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i + 1) % 6]

        # Calculate the wall's normal vector
        wall_vector = [p2[0] - p1[0], p2[1] - p1[1]]
        wall_normal = [-wall_vector[1], wall_vector[0]]
        wall_normal = normalize(wall_normal)

        # Check if the ball is colliding with the wall
        wall_length = math.sqrt(wall_vector[0] ** 2 + wall_vector[1] ** 2)
        wall_unit_vector = [wall_vector[0] / wall_length, wall_vector[1] / wall_length]
        ball_to_wall = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]
        projection_length = (
            ball_to_wall[0] * wall_unit_vector[0] + ball_to_wall[1] * wall_unit_vector[1]
        )

        if 0 <= projection_length <= wall_length:
            closest_point = [
                p1[0] + projection_length * wall_unit_vector[0],
                p1[1] + projection_length * wall_unit_vector[1],
            ]
            distance_to_wall = math.sqrt(
                (ball_pos[0] - closest_point[0]) ** 2
                + (ball_pos[1] - closest_point[1]) ** 2
            )

            if distance_to_wall <= ball_radius:
                # Reflect the ball's velocity
                ball_vel = reflect_velocity(ball_vel, wall_normal)
                ball_vel[0] *= friction
                ball_vel[1] *= friction

                # Move the ball out of the wall
                overlap = ball_radius - distance_to_wall
                ball_pos[0] += wall_normal[0] * overlap
                ball_pos[1] += wall_normal[1] * overlap

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
