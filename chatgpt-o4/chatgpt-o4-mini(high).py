import math
import pygame

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
HEX_RADIUS = 200
NUM_SIDES = 6
BALL_RADIUS = 15

GRAVITY = 500.0            # pixels/s²
AIR_FRICTION = 0.05        # per second
RESTITUTION = 0.9          # coefficient of restitution
SPIN_RATE = math.radians(30)  # rad/s

FPS = 60

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()

# Precompute hexagon in local coords
hexagon = [
    (
        HEX_RADIUS * math.cos(2 * math.pi * i / NUM_SIDES),
        HEX_RADIUS * math.sin(2 * math.pi * i / NUM_SIDES),
    )
    for i in range(NUM_SIDES)
]

center = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
angle = 0.0

# Ball state
ball_pos = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
ball_vel = pygame.math.Vector2(150, -50)

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    # --- Physics update ---
    angle += SPIN_RATE * dt

    # Gravity
    ball_vel.y += GRAVITY * dt
    # Simple air friction
    ball_vel *= max(0.0, 1.0 - AIR_FRICTION * dt)
    # Position
    ball_pos += ball_vel * dt

    # Compute rotated hexagon vertices
    verts = []
    for x, y in hexagon:
        rx = x * math.cos(angle) - y * math.sin(angle) + center.x
        ry = x * math.sin(angle) + y * math.cos(angle) + center.y
        verts.append(pygame.math.Vector2(rx, ry))

    # Collision: edges then corners
    collided = False
    for i in range(NUM_SIDES):
        p1 = verts[i]
        p2 = verts[(i + 1) % NUM_SIDES]
        edge = p2 - p1
        # inward normal for CCW polygon
        normal = pygame.math.Vector2(-edge.y, edge.x)
        normal.normalize_ip()

        to_ball = ball_pos - p1
        dist = to_ball.dot(normal)
        # projection factor to check segment bounds
        proj = ball_pos - normal * dist
        t = (proj - p1).dot(edge) / edge.dot(edge)

        if dist < BALL_RADIUS and 0.0 <= t <= 1.0:
            # relative velocity at collision point
            r = proj - center
            v_wall = pygame.math.Vector2(-SPIN_RATE * r.y, SPIN_RATE * r.x)
            v_rel = ball_vel - v_wall
            vn = v_rel.dot(normal)
            if vn < 0.0:
                # reflect
                v_rel -= (1 + RESTITUTION) * vn * normal
                ball_vel = v_rel + v_wall
                # push out
                ball_pos += normal * (BALL_RADIUS - dist)
                collided = True
                break

    if not collided:
        # corner collisions
        for p in verts:
            diff = ball_pos - p
            d = diff.length()
            if d < BALL_RADIUS and d > 1e-6:
                normal = diff / d
                r = p - center
                v_wall = pygame.math.Vector2(-SPIN_RATE * r.y, SPIN_RATE * r.x)
                v_rel = ball_vel - v_wall
                vn = v_rel.dot(normal)
                if vn < 0.0:
                    v_rel -= (1 + RESTITUTION) * vn * normal
                    ball_vel = v_rel + v_wall
                    ball_pos += normal * (BALL_RADIUS - d)
                break

    # --- Drawing ---
    screen.fill((30, 30, 30))
    # draw hexagon
    pygame.draw.polygon(
        screen, (200, 200, 200), [(v.x, v.y) for v in verts], width=2
    )
    # draw ball
    pygame.draw.circle(
        screen,
        (255, 100, 100),
        (int(ball_pos.x), int(ball_pos.y)),
        BALL_RADIUS,
    )

    pygame.display.flip()

pygame.quit()