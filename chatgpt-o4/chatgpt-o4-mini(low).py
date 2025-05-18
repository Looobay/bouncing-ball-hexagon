import sys
import math
import pygame

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

# Hexagon parameters
HEX_RADIUS = 250
HEX_CENTER = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
ANGULAR_SPEED = math.radians(30)  # 30° per second

# Ball parameters
ball_pos = pygame.math.Vector2(WIDTH // 2, 100)
ball_vel = pygame.math.Vector2(200, 0)
BALL_RADIUS = 15

GRAVITY = pygame.math.Vector2(0, 500)  # px/s²
FRICTION = 0.999  # per frame

def hex_vertices(angle):
    """Return list of 6 vertices of the rotated hexagon."""
    verts = []
    for i in range(6):
        theta = angle + i * math.radians(60)
        x = HEX_CENTER.x + HEX_RADIUS * math.cos(theta)
        y = HEX_CENTER.y + HEX_RADIUS * math.sin(theta)
        verts.append(pygame.math.Vector2(x, y))
    return verts

def reflect(ball_vel, normal):
    """Reflect velocity about normal: v' = v - 2(v·n)n."""
    # In comments with LaTeX: \( \mathbf v' = \mathbf v 
    # - 2 (\mathbf v\cdot \mathbf n)\,\mathbf n\)
    return ball_vel - 2 * ball_vel.dot(normal) * normal

def wall_velocity(pt, angle):
    """Instantaneous velocity of a point on the rotating hexagon."""
    # v = ω × r  (in 2D, perpendicular)
    rel = pt - HEX_CENTER
    # Perp vector: (-y, x)
    perp = pygame.math.Vector2(-rel.y, rel.x)
    return ANGULAR_SPEED * perp

def main():
    angle = 0.0
    running = True
    while running:
        dt = CLOCK.tick(60) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # Update hexagon rotation
        angle += ANGULAR_SPEED * dt
        verts = hex_vertices(angle)
        edges = [(verts[i], verts[(i+1)%6]) for i in range(6)]

        # Apply gravity and friction
        ball_vel.y += GRAVITY.y * dt
        ball_vel *= FRICTION

        # Move ball
        ball_pos.xy += ball_vel * dt

        # Collision with each edge
        for a, b in edges:
            # Edge vector and normal (inward)
            edge = b - a
            normal = pygame.math.Vector2(edge.y, -edge.x).normalize()
            # Ensure normal points inward
            if (HEX_CENTER - a).dot(normal) < 0:
                normal = -normal

            # Distance from ball center to infinite line
            dist = (ball_pos - a).dot(normal)
            # Projected point
            proj = ball_pos - dist * normal

            # Check collision if within segment & penetrating
            if (0 < (proj - a).dot(edge) < edge.length_squared()
                    and dist < BALL_RADIUS):
                # Relative velocity
                v_wall = wall_velocity(proj, angle)
                v_rel = ball_vel - v_wall
                # Reflect relative velocity
                v_rel_ref = reflect(v_rel, normal)
                # New absolute velocity
                ball_vel.xy = v_rel_ref + v_wall
                # Push ball outside
                ball_pos += (BALL_RADIUS - dist) * normal

        # Drawing
        SCREEN.fill((30, 30, 30))
        # Hexagon
        pygame.draw.polygon(SCREEN, (200, 200, 200), verts, 4)
        # Ball
        pygame.draw.circle(SCREEN, (200, 50, 50),
                           (int(ball_pos.x), int(ball_pos.y)),
                           BALL_RADIUS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()