import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mistral7B - Le Chat (28/02/2025)")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Pymunk space
space = pymunk.Space()
space.gravity = (0.0, 900.0)

# Drawing utilities
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Hexagon properties
hexagon_radius = 150
hexagon_vertices = 6
hexagon_angle = 0
hexagon_angular_velocity = math.pi / 180  # 1 degree per frame

# Ball properties
ball_radius = 10
ball_mass = 1
ball_elasticity = 0.8
ball_friction = 0.9

# Create the ball
ball_body = pymunk.Body(ball_mass, pymunk.moment_for_circle(ball_mass, 0, ball_radius))
ball_body.position = (WIDTH / 2, HEIGHT / 2)
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = ball_elasticity
ball_shape.friction = ball_friction
space.add(ball_body, ball_shape)

# Function to create hexagon vertices
def create_hexagon_vertices(radius, angle):
    vertices = []
    for i in range(hexagon_vertices):
        x = WIDTH / 2 + radius * math.cos(angle + 2 * math.pi * i / hexagon_vertices)
        y = HEIGHT / 2 + radius * math.sin(angle + 2 * math.pi * i / hexagon_vertices)
        vertices.append((x, y))
    return vertices

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon angle
    hexagon_angle += hexagon_angular_velocity

    # Create hexagon vertices
    hexagon_vertices = create_hexagon_vertices(hexagon_radius, hexagon_angle)

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the hexagon
    pygame.draw.polygon(screen, (0, 0, 0), hexagon_vertices, 2)

    # Update physics
    space.step(1 / FPS)

    # Draw the ball
    pos = ball_body.position
    pygame.draw.circle(screen, (255, 0, 0), (int(pos.x), int(pos.y)), ball_radius)

    # Check for collisions with hexagon walls
    for i in range(hexagon_vertices):
        start = hexagon_vertices[i]
        end = hexagon_vertices[(i + 1) % hexagon_vertices]
        segment_shape = pymunk.Segment(space.static_body, start, end, 2)
        segment_shape.elasticity = 0.8
        segment_shape.friction = 0.9
        space.add(segment_shape)

    # Draw the space (for debugging)
    space.debug_draw(draw_options)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
