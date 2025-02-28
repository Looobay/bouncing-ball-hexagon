import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ChatGPT o3 mini (low) (28/02/2025)")

# Colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
BLUE  = (  0,   0, 255)

# Physics constants
GRAVITY = 0.5       # gravitational acceleration
FRICTION = 0.99     # friction factor applied after collisions

# Ball settings
ball_radius = 10
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [4, -2]

# Hexagon settings
hex_radius = 200  # distance from center to vertex
hex_center = (WIDTH/2, HEIGHT/2)
hex_angle = 0  # current rotation angle (in radians)
hex_spin_speed = 0.01  # radians per frame

clock = pygame.time.Clock()
FPS = 60

def get_hexagon_points(center, radius, angle):
    """Return list of 6 points for a hexagon centered at center,
    with a given radius and rotated by angle."""
    cx, cy = center
    points = []
    for i in range(6):
        theta = math.pi/6 + i * math.pi / 3 + angle  # start rotated by 30° for flat top
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        points.append((x, y))
    return points

def point_line_distance(p, a, b):
    """Return the distance from point p to the line segment a-b and also
    the closest point on the line."""
    # Compute the projection of point p onto line ab
    ax, ay = a
    bx, by = b
    px, py = p
    # Vector from a -> p and a -> b
    abx, aby = bx - ax, by - ay
    apx, apy = px - ax, py - ay
    ab_length2 = abx * abx + aby * aby

    # Avoid division by zero if a and b are the same
    if ab_length2 == 0:
        return math.hypot(px - ax, py - ay), a

    # projection fraction
    t = (apx * abx + apy * aby) / ab_length2

    # Clamp t to [0,1] to find the closest point on the segment
    t = max(0, min(1, t))
    closest = (ax + t * abx, ay + t * aby)
    dist = math.hypot(px - closest[0], py - closest[1])
    return dist, closest

def reflect_vector(v, normal):
    """Reflect the vector v from a surface with the given normal.
    v and normal are 2-tuples"""
    # normalize normal
    nx, ny = normal
    mag = math.hypot(nx, ny)
    if mag == 0:
        return v
    nx /= mag
    ny /= mag
    # Dot product
    dot = v[0] * nx + v[1] * ny
    # reflection: v - 2*(v dot n)*n
    rx = v[0] - 2 * dot * nx
    ry = v[1] - 2 * dot * ny
    return [rx, ry]

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation angle
    hex_angle += hex_spin_speed
    hex_points = get_hexagon_points(hex_center, hex_radius, hex_angle)

    # Update ball physics: apply gravity
    ball_vel[1] += GRAVITY
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Collision detection with hexagon walls
    for i in range(len(hex_points)):
        a = hex_points[i]
        b = hex_points[(i + 1) % len(hex_points)]
        dist, closest = point_line_distance(ball_pos, a, b)
        if dist <= ball_radius:
            # Determine the wall normal (pointing outward)
            # For a convex polygon, the normal can be computed as a perpendicular
            # to the edge. We'll choose the one pointing from the wall towards the ball.
            edge_vec = (b[0] - a[0], b[1] - a[1])
            normal = (-edge_vec[1], edge_vec[0])
            # Check if the normal is indeed pointing toward the ball.
            # Compute vector from closest point to ball:
            cp_to_ball = (ball_pos[0] - closest[0], ball_pos[1] - closest[1])
            # If dot product is negative, flip the normal
            dot = normal[0]*cp_to_ball[0] + normal[1]*cp_to_ball[1]
            if dot < 0:
                normal = (-normal[0], -normal[1])

            # Reflect ball velocity
            ball_vel = reflect_vector(ball_vel, normal)
            # Apply friction multiplier
            ball_vel[0] *= FRICTION
            ball_vel[1] *= FRICTION
            # Move ball out of collision (simple correction)
            overlap = ball_radius - dist + 1
            ball_pos[0] += normal[0] / math.hypot(*normal) * overlap
            ball_pos[1] += normal[1] / math.hypot(*normal) * overlap

    # Optional: Bounce off screen boundaries in case the ball escapes the hexagon.
    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > WIDTH:
        ball_vel[0] = -ball_vel[0] * FRICTION
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > HEIGHT:
        ball_vel[1] = -ball_vel[1] * FRICTION

    # Clear screen
    screen.fill(BLACK)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hex_points, width=2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])),
                       ball_radius)

    pygame.display.flip()

pygame.quit()
sys.exit()