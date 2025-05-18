import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball inside Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
HEX_COLOR = (0, 128, 255)

# Physics parameters
GRAVITY = 0.5
FRICTION = 0.99
BOUNCE_DAMPING = 0.8

# Hexagon parameters
HEX_RADIUS = 200
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
rotation_angle = 0
rotation_speed = 0.01  # radians per frame

# Ball parameters
ball_pos = [WIDTH // 2, HEIGHT // 4]
ball_vel = [2, 0]
ball_radius = 15

clock = pygame.time.Clock()

def get_hexagon_points(center, radius, angle):
    """Calculate the vertices of a hexagon rotated by 'angle'."""
    points = []
    for i in range(6):
        theta = math.pi / 3 * i + angle
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    return points

def get_edges(points):
    """Return list of edges as pairs of points."""
    edges = []
    for i in range(len(points)):
        start = points[i]
        end = points[(i + 1) % len(points)]
        edges.append((start, end))
    return edges

def rotate_point(point, center, angle):
    """Rotate a point around a center by 'angle'."""
    s = math.sin(angle)
    c = math.cos(angle)
    px, py = point[0] - center[0], point[1] - center[1]
    xnew = px * c - py * s
    ynew = px * s + py * c
    return (xnew + center[0], ynew + center[1])

def get_normal_vector(p1, p2):
    """Get the outward normal vector of an edge."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # Normal vector (perpendicular)
    normal = (-dy, dx)
    length = math.hypot(normal[0], normal[1])
    return (normal[0] / length, normal[1] / length)

def project_point_on_axis(point, axis):
    """Project a point onto an axis."""
    return point[0] * axis[0] + point[1] * axis[1]

def check_collision(ball_pos, ball_vel, edges):
    """Check collision with edges and reflect velocity if needed."""
    for start, end in edges:
        # Calculate edge vector and normal
        edge_vec = (end[0] - start[0], end[1] - start[1])
        normal = get_normal_vector(start, end)

        # Vector from start to ball center
        to_ball = (ball_pos[0] - start[0], ball_pos[1] - start[1])

        # Distance from ball to edge along normal
        dist = to_ball[0] * normal[0] + to_ball[1] * normal[1]

        # Check if ball is penetrating the edge
        if abs(dist) <= ball_radius:
            # Check if the projection of the ball center onto the edge lies within the edge segment
            edge_length = math.hypot(edge_vec[0], edge_vec[1])
            proj = (to_ball[0] * edge_vec[0] + to_ball[1] * edge_vec[1]) / edge_length
            if 0 <= proj <= edge_length:
                # Reflect velocity
                vel_dot_normal = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
                ball_vel[0] -= 2 * vel_dot_normal * normal[0]
                ball_vel[1] -= 2 * vel_dot_normal * normal[1]
                # Apply damping
                ball_vel[0] *= BOUNCE_DAMPING
                ball_vel[1] *= BOUNCE_DAMPING
                # Push the ball out of collision
                overlap = ball_radius - abs(dist)
                ball_pos[0] += normal[0] * overlap
                ball_pos[1] += normal[1] * overlap

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update rotation angle
    rotation_angle += rotation_speed

    # Get current hexagon points
    hex_points = get_hexagon_points(HEX_CENTER, HEX_RADIUS, rotation_angle)
    edges = get_edges(hex_points)

    # Physics update
    ball_vel[1] += GRAVITY  # gravity
    ball_vel[0] *= FRICTION
    ball_vel[1] *= FRICTION

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Check collision with hexagon walls
    check_collision(ball_pos, ball_vel, edges)

    # Keep ball inside window bounds
    if ball_pos[0] - ball_radius < 0:
        ball_pos[0] = ball_radius
        ball_vel[0] *= -BOUNCE_DAMPING
    elif ball_pos[0] + ball_radius > WIDTH:
        ball_pos[0] = WIDTH - ball_radius
        ball_vel[0] *= -BOUNCE_DAMPING
    if ball_pos[1] - ball_radius < 0:
        ball_pos[1] = ball_radius
        ball_vel[1] *= -BOUNCE_DAMPING
    elif ball_pos[1] + ball_radius > HEIGHT:
        ball_pos[1] = HEIGHT - ball_radius
        ball_vel[1] *= -BOUNCE_DAMPING

    # Drawing
    screen.fill(WHITE)

    # Draw rotating hexagon
    pygame.draw.polygon(screen, HEX_COLOR, hex_points, 3)

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    pygame.display.flip()
    clock.tick(60)