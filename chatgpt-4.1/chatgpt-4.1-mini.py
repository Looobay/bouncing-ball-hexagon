import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing Inside a Spinning Hexagon")

clock = pygame.time.Clock()
FPS = 60

# Colors
BG_COLOR = (30, 30, 30)
HEX_COLOR = (200, 200, 200)
BALL_COLOR = (255, 100, 100)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.99  # air friction
BOUNCE_FRICTION = 0.8  # energy loss on bounce

# Hexagon parameters
HEX_RADIUS = 200
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_SIDES = 6
ROTATION_SPEED = 0.01  # radians per frame


def rotate_point(cx, cy, x, y, angle):
    """Rotate point (x,y) around (cx,cy) by angle radians."""
    s = math.sin(angle)
    c = math.cos(angle)

    # translate point back to origin:
    x -= cx
    y -= cy

    # rotate point
    x_new = x * c - y * s
    y_new = x * s + y * c

    # translate point back:
    x_new += cx
    y_new += cy
    return x_new, y_new


def polygon_points(center, radius, sides, rotation):
    """Return list of points for a regular polygon."""
    points = []
    angle_between = 2 * math.pi / sides
    for i in range(sides):
        angle = angle_between * i + rotation
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points


def line_normal(p1, p2):
    """Calculate outward normal vector of the line from p1 to p2."""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    length = math.hypot(dx, dy)
    # Normal vector (perpendicular)
    nx = -dy / length
    ny = dx / length
    return nx, ny


def reflect_vector(vx, vy, nx, ny):
    """Reflect vector (vx, vy) about normal (nx, ny)."""
    # v' = v - 2(v·n)n
    dot = vx * nx + vy * ny
    rx = vx - 2 * dot * nx
    ry = vy - 2 * dot * ny
    return rx, ry


class Ball:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 3
        self.vy = 0

    def update(self):
        # Apply gravity
        self.vy += GRAVITY

        # Apply air friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)), self.radius)

    def collide_with_polygon(self, poly_points):
        # Check collision with each edge of polygon
        for i in range(len(poly_points)):
            p1 = poly_points[i]
            p2 = poly_points[(i + 1) % len(poly_points)]

            # Vector from p1 to p2
            edge_dx = p2[0] - p1[0]
            edge_dy = p2[1] - p1[1]

            # Vector from p1 to ball center
            ball_dx = self.x - p1[0]
            ball_dy = self.y - p1[1]

            edge_length = math.hypot(edge_dx, edge_dy)
            edge_dir_x = edge_dx / edge_length
            edge_dir_y = edge_dy / edge_length

            # Project ball vector onto edge
            proj = ball_dx * edge_dir_x + ball_dy * edge_dir_y

            # Clamp projection to edge segment
            proj = max(0, min(edge_length, proj))

            # Closest point on edge to ball center
            closest_x = p1[0] + proj * edge_dir_x
            closest_y = p1[1] + proj * edge_dir_y

            # Distance from ball center to closest point
            dist_x = self.x - closest_x
            dist_y = self.y - closest_y
            dist = math.hypot(dist_x, dist_y)

            if dist < self.radius:
                # Collision detected
                # Calculate normal (pointing outward)
                nx, ny = line_normal(p1, p2)

                # Check if ball is inside polygon or outside
                # We want to push ball outside, so check direction of normal relative to ball velocity
                # If dot product of normal and ball velocity is positive, normal points inward, flip it
                if (self.vx * nx + self.vy * ny) > 0:
                    nx, ny = -nx, -ny

                # Push ball out of collision
                overlap = self.radius - dist
                self.x += nx * overlap
                self.y += ny * overlap

                # Reflect velocity vector about normal
                self.vx, self.vy = reflect_vector(self.vx, self.vy, nx, ny)

                # Apply bounce friction (energy loss)
                self.vx *= BOUNCE_FRICTION
                self.vy *= BOUNCE_FRICTION


def main():
    ball = Ball(WIDTH // 2, HEIGHT // 2 - 100)

    rotation = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update rotation
        rotation += ROTATION_SPEED
        rotation %= 2 * math.pi

        # Get hexagon points
        hex_points = polygon_points(HEX_CENTER, HEX_RADIUS, HEX_SIDES, rotation)

        # Update ball physics
        ball.update()

        # Collision detection and response
        ball.collide_with_polygon(hex_points)

        # Draw hexagon
        pygame.draw.polygon(screen, HEX_COLOR, hex_points, 3)

        # Draw ball
        ball.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()