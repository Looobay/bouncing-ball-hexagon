import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Grok 3 - Thinking (28/02/2025)")
clock = pygame.time.Clock()

# Initialize Pymunk space
space = pymunk.Space()
space.gravity = (0, -900)  # Gravity downwards in Pymunk coordinates

# Create the spinning hexagon
center = (400, 300)  # Center of the screen in Pymunk coordinates
hexagon_radius = 200  # Radius of the hexagon (distance from center to vertex)
hexagon_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
hexagon_body.position = center
hexagon_body.angular_velocity = 1.0  # Angular velocity in radians per second (counterclockwise)

# Define hexagon vertices in local coordinates
vertices = [
    (hexagon_radius * math.cos(2 * math.pi * i / 6),
     hexagon_radius * math.sin(2 * math.pi * i / 6))
    for i in range(6)
]

# Create segment shapes for the hexagon sides
segments = []
for i in range(6):
    start = vertices[i]
    end = vertices[(i + 1) % 6]
    segment = pymunk.Segment(hexagon_body, start, end, 5)  # Thickness of 5 for collision
    segment.elasticity = 0.8  # Inelastic collisions to simulate energy loss
    segment.friction = 0.5    # Friction during contact
    segments.append(segment)

# Add hexagon body and segments to the space
space.add(hexagon_body, *segments)

# Create the ball
ball_radius = 10
ball_mass = 1
ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
ball_body = pymunk.Body(ball_mass, ball_moment)
ball_body.position = (center[0], center[1] + 100)  # Start above the center
ball_shape = pymunk.Circle(ball_body, ball_radius)
ball_shape.elasticity = 0.8  # Inelastic collisions
ball_shape.friction = 0.5    # Friction during contact

# Add ball to the space
space.add(ball_body, ball_shape)

# Optional: Give the ball an initial velocity
ball_body.velocity = (100, 0)  # Initial horizontal velocity

# Set up Pymunk drawing options for Pygame
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update physics simulation
    dt = 1.0 / 60.0  # Time step (60 FPS)
    space.step(dt)

    # Render the scene
    screen.fill((255, 255, 255))  # White background
    space.debug_draw(draw_options)  # Draw all Pymunk objects
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Clean up
pygame.quit()