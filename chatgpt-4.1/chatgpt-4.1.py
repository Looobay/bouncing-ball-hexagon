import pygame
import math
import sys

# --- Constants ---
WIDTH, HEIGHT = 800, 800
FPS = 60

HEX_RADIUS = 300
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_SIDES = 6

BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.98
BOUNCE_DAMPING = 0.85  # Energy loss on bounce

SPIN_SPEED = 0.01  # Radians per frame

# --- Helper Functions ---
def rotate_point(cx, cy, angle, px, py):
    """Rotate point (px, py) around (cx, cy) by angle (radians)."""
    s, c = math.sin(angle), math.cos(angle)
    px, py = px - cx, py - cy
    xnew = px * c - py * s
    ynew = px * s + py * c
    return xnew + cx, ynew + cy

def get_hexagon_points(center, radius, angle):
    """Return the 6 points of a rotated hexagon."""
    points = []
    for i in range(HEX_SIDES):
        theta = angle + i * (2 * math.pi / HEX_SIDES)
        x = center[0] + radius * math.cos(theta)
        y = center[1] + radius * math.sin(theta)
        points.append((x, y))
    return points

def reflect_velocity(velocity, normal):
    """Reflect velocity vector off a surface with given normal."""
    v_dot_n = velocity[0] * normal[0] + velocity[1] * normal[1]
    return (
        velocity[0] - 2 * v_dot_n * normal[0],
        velocity[1] - 2 * v_dot_n * normal[1],
    )

# --- Ball Class ---
class Ball:
    def __init__(self, pos, vel):
        self.pos = list(pos)
        self.vel = list(vel)
        self.radius = BALL_RADIUS

    def update(self):
        self.vel[1] += GRAVITY
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

    def apply_friction(self):
        self.vel[0] *= FRICTION
        self.vel[1] *= FRICTION

    def draw(self, surface):
        pygame.draw.circle(
            surface, (255, 100, 100), (int(self.pos[0]), int(self.pos[1])), self.radius
        )

# --- Main Program ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball((WIDTH // 2, HEIGHT // 2 - 100), (5, 0))
    hex_angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update hexagon rotation
        hex_angle += SPIN_SPEED

        # Update ball physics
        ball.update()

        # Get hexagon points
        hex_points = get_hexagon_points(HEX_CENTER, HEX_RADIUS, hex_angle)

        # Collision detection: check each wall
        for i in range(HEX_SIDES):
            p1 = hex_points[i]
            p2 = hex_points[(i + 1) % HEX_SIDES]

            # Wall vector and normal
            wall_vec = (p2[0] - p1[0], p2[1] - p1[1])
            wall_len = math.hypot(*wall_vec)
            wall_dir = (wall_vec[0] / wall_len, wall_vec[1] / wall_len)
            normal = (-wall_dir[1], wall_dir[0])  # Perpendicular (outward)

            # Closest point on wall to ball
            ball_to_p1 = (ball.pos[0] - p1[0], ball.pos[1] - p1[1])
            proj = ball_to_p1[0] * wall_dir[0] + ball_to_p1[1] * wall_dir[1]
            proj = max(0, min(wall_len, proj))
            closest = (p1[0] + wall_dir[0] * proj, p1[1] + wall_dir[1] * proj)

            # Distance to wall
            dist = math.hypot(ball.pos[0] - closest[0], ball.pos[1] - closest[1])

            if dist < ball.radius:
                # Move ball out of wall
                overlap = ball.radius - dist + 1
                ball.pos[0] += normal[0] * overlap
                ball.pos[1] += normal[1] * overlap

                # Reflect velocity
                ball.vel = reflect_velocity(ball.vel, normal)
                ball.vel = (ball.vel[0] * BOUNCE_DAMPING, ball.vel[1] * BOUNCE_DAMPING)
                ball.apply_friction()

        # Drawing
        screen.fill((30, 30, 40))
        pygame.draw.polygon(screen, (100, 200, 255), hex_points, 6)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()