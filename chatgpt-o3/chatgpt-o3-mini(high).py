import math
import pygame
import sys

# Initialize Pygame.
pygame.init()

# Screen settings.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ChatGPT o3 mini (high) (28/02/2025)")

# Colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Physics parameters.
GRAVITY = 500.0  # pixels/s^2 downward
RESTITUTION = 0.9  # bounce energy retention for the normal component
TANGENT_FRICTION = 0.98  # friction on the tangential component at impact
AIR_FRICTION = 0.999  # continuous (air) friction

# Hexagon parameters.
HEX_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
HEX_RADIUS = 250
hex_rotation = 0.0  # current rotation angle in radians
angular_velocity = math.radians(30)  # hexagon rotates at 30° per second

# Ball parameters.
ball = {
    "pos": [HEX_CENTER[0], HEX_CENTER[1] - 100],
    "vel": [200.0, 0.0],
    "radius": 15,
}

clock = pygame.time.Clock()


def get_hexagon_vertices(cx, cy, radius, rotation):
    """
    Compute the vertices of a regular hexagon with center (cx,cy),
    given radius (distance from center to vertex), and rotated by 'rotation'
    radians.
    """
    vertices = []
    for i in range(6):
        angle = rotation + math.radians(60 * i)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices


def closest_point_on_segment(p, a, b):
    """
    Given point p and line segment ab, return the closest point on the segment.
    p, a, and b are each 2-tuples (x, y).
    """
    (px, py) = p
    (ax, ay) = a
    (bx, by) = b
    dx = bx - ax
    dy = by - ay
    if dx == 0 and dy == 0:
        return a
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    return (ax + t * dx, ay + t * dy)


running = True
while running:
    dt = clock.tick(60) / 1000.0  # delta time in seconds (target 60 FPS)

    # Event handling.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the hexagon's rotation.
    hex_rotation += angular_velocity * dt

    # Update the ball's velocity (gravity) and position.
    ball["vel"][1] += GRAVITY * dt
    ball["pos"][0] += ball["vel"][0] * dt
    ball["pos"][1] += ball["vel"][1] * dt

    # Optionally apply air friction.
    ball["vel"][0] *= AIR_FRICTION
    ball["vel"][1] *= AIR_FRICTION

    # Compute hexagon vertices (with updated rotation).
    vertices = get_hexagon_vertices(
        HEX_CENTER[0], HEX_CENTER[1], HEX_RADIUS, hex_rotation
    )

    # Check for collisions against each edge of the hexagon.
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        # Find the closest point on the edge segment to the ball center.
        cp = closest_point_on_segment(ball["pos"], p1, p2)
        dx = ball["pos"][0] - cp[0]
        dy = ball["pos"][1] - cp[1]
        dist = math.hypot(dx, dy)

        if dist < ball["radius"]:
            # Avoid division by zero.
            if dist == 0:
                dist = 0.01
            penetration = ball["radius"] - dist
            # Collision normal: from the contact point toward the ball center.
            normal = (dx / dist, dy / dist)
            # Push the ball out so that it is just touching the wall.
            ball["pos"][0] += normal[0] * penetration
            ball["pos"][1] += normal[1] * penetration

            # Compute the wall's velocity at the contact point.
            # For a rotating hexagon around HEX_CENTER, the velocity is given by
            # v = ω × r, which in 2D is: v = (-ω*(py-cy), ω*(px-cx)).
            v_wall = (
                -angular_velocity * (cp[1] - HEX_CENTER[1]),
                angular_velocity * (cp[0] - HEX_CENTER[0]),
            )

            # Compute ball velocity relative to the wall.
            v_rel = (
                ball["vel"][0] - v_wall[0],
                ball["vel"][1] - v_wall[1],
            )

            # Decompose relative velocity into components normal and tangential
            # to the collision.
            v_rel_norm = v_rel[0] * normal[0] + v_rel[1] * normal[1]
            v_rel_norm_vec = (v_rel_norm * normal[0], v_rel_norm * normal[1])
            v_rel_tan = (
                v_rel[0] - v_rel_norm_vec[0],
                v_rel[1] - v_rel_norm_vec[1],
            )

            # Reflect the normal component (with energy loss) and apply friction
            # to the tangential component.
            new_v_rel_norm = -RESTITUTION * v_rel_norm
            new_v_rel_tan = (TANGENT_FRICTION * v_rel_tan[0],
                             TANGENT_FRICTION * v_rel_tan[1])

            # The new relative velocity is the sum of the components.
            new_v_rel = (new_v_rel_norm * normal[0] + new_v_rel_tan[0],
                         new_v_rel_norm * normal[1] + new_v_rel_tan[1])
            # Set the ball's new velocity in the absolute frame.
            ball["vel"][0] = v_wall[0] + new_v_rel[0]
            ball["vel"][1] = v_wall[1] + new_v_rel[1]

    # Drawing.
    screen.fill(BLACK)
    # Draw hexagon (outline).
    pygame.draw.polygon(screen, WHITE, vertices, 3)
    # Draw ball.
    pygame.draw.circle(
        screen,
        RED,
        (int(ball["pos"][0]), int(ball["pos"][1])),
        ball["radius"],
    )
    pygame.display.flip()

pygame.quit()
sys.exit()