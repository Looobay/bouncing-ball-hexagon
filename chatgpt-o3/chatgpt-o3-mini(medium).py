import pygame
import math
import sys

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 500            # pixels/s², acceleration downwards
FRICTION = 0.99          # general damping on the ball (not applied on collisions)
ELASTICITY = 0.9         # energy loss factor when bouncing
BALL_RADIUS = 15

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
clock = pygame.time.Clock()

# Ball properties (starting near the center with an initial velocity)
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [200, -150]  # pixels per second

# Hexagon properties
hex_center = (WIDTH / 2, HEIGHT / 2)
hex_radius = 250
hex_rotation = 0  # Initial rotation angle (in radians)
rotation_speed = math.radians(30)  # Rotation speed (30°/s in radians)

def get_hexagon_vertices(center, radius, angle):
    """
    Returns the vertices of a regular hexagon centered at 'center' 
    with given 'radius' and rotated by 'angle' radians.
    """
    cx, cy = center
    vertices = []
    for i in range(6):
        theta = angle + math.radians(60 * i)
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

def reflect(vel, normal):
    """
    Reflect a velocity vector 'vel' about the wall's unit normal 'normal'.
    Uses the formula:
    
    v' = v - 2 (v ⋅ n) n
    """
    # Ensure the normal is a unit vector
    norm_length = math.hypot(normal[0], normal[1])
    if norm_length == 0:
        return vel
    n = (normal[0] / norm_length, normal[1] / norm_length)
    dot = vel[0] * n[0] + vel[1] * n[1]
    reflected = (vel[0] - 2 * dot * n[0], vel[1] - 2 * dot * n[1])
    return reflected

def point_line_distance(point, line_start, line_end):
    """
    Returns the distance from 'point' to the line segment defined by
    'line_start' and 'line_end', along with the closest point on this segment.
    """
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end
    line_mag = math.hypot(x2 - x1, y2 - y1)
    if line_mag < 1e-8:
        return math.hypot(px - x1, py - y1), (x1, y1)
    # Project point onto the line (parameterized by u)
    u = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / (line_mag * line_mag)
    if u < 0:
        closest = (x1, y1)
    elif u > 1:
        closest = (x2, y2)
    else:
        closest = (x1 + u * (x2 - x1), y1 + u * (y2 - y1))
    distance = math.hypot(px - closest[0], py - closest[1])
    return distance, closest

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0  # delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the hexagon continuously
    hex_rotation += rotation_speed * dt

    # Update ball dynamics: apply gravity and friction
    ball_vel[1] += GRAVITY * dt
    ball_vel[0] *= FRICTION
    ball_vel[1] *= FRICTION

    # Update ball's position based on its velocity
    ball_pos[0] += ball_vel[0] * dt
    ball_pos[1] += ball_vel[1] * dt

    # Get current hexagon vertices (rotating)
    vertices = get_hexagon_vertices(hex_center, hex_radius, hex_rotation)

    # Check collisions with each wall of the hexagon
    for i in range(len(vertices)):
        start = vertices[i]
        end = vertices[(i + 1) % len(vertices)]
        dist, closest = point_line_distance(ball_pos, start, end)
        if dist < BALL_RADIUS:
            # Calculate the wall vector
            wx = end[0] - start[0]
            wy = end[1] - start[1]
            # Two possible perpendiculars: (-wy, wx) and (wy, -wx)
            # Choose the one pointing inward.
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            center_vec = (hex_center[0] - midpoint[0], hex_center[1] - midpoint[1])
            n1 = (-wy, wx)
            n2 = (wy, -wx)
            dot1 = n1[0] * center_vec[0] + n1[1] * center_vec[1]
            dot2 = n2[0] * center_vec[0] + n2[1] * center_vec[1]
            if dot1 < dot2:
                wall_normal = n2
            else:
                wall_normal = n1

            # Normalize the wall normal
            norm_length = math.hypot(wall_normal[0], wall_normal[1])
            if norm_length != 0:
                normal_unit = (wall_normal[0] / norm_length,
                               wall_normal[1] / norm_length)
            else:
                normal_unit = (0, 0)

            # Only reflect if the ball is moving towards the wall
            if (ball_vel[0] * normal_unit[0] +
                    ball_vel[1] * normal_unit[1]) < 0:
                # Reflect the ball's velocity and apply energy loss
                ball_vel = list(reflect(ball_vel, normal_unit))
                ball_vel[0] *= ELASTICITY
                ball_vel[1] *= ELASTICITY

                # Adjust the ball's position so it is no longer intersecting
                overlap = BALL_RADIUS - dist
                ball_pos[0] += normal_unit[0] * overlap
                ball_pos[1] += normal_unit[1] * overlap

    # Clear the screen
    screen.fill(BLACK)

    # Draw the spinning hexagon
    pygame.draw.polygon(screen, WHITE, vertices, 3)

    # Draw the ball
    pygame.draw.circle(
        screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS
    )

    pygame.display.flip()

pygame.quit()
sys.exit()