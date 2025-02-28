import math
import pygame

# ----- Configuration Parameters -----
WIDTH, HEIGHT = 800, 600
FPS = 60

# Ball parameters
BALL_RADIUS = 12
BALL_COLOR = (255, 50, 50)
INITIAL_BALL_POS = pygame.math.Vector2(WIDTH//2, HEIGHT//2 - 100)
INITIAL_BALL_VEL = pygame.math.Vector2(120, 10)

# Physics parameters
GRAVITY = pygame.math.Vector2(0, 500)  # pixels per second^2
RESTITUTION = 0.9  # bounce (energy retention) in normal direction
FRICTION_COEF = 0.2  # fraction of tangential velocity lost on collision

# Hexagon parameters
HEX_CENTER = pygame.math.Vector2(WIDTH//2, HEIGHT//2)
HEX_RADIUS = 200  # distance from center to vertex
HEX_SIDES = 6
HEX_COLOR = (50, 200, 50)
HEX_THICKNESS = 3
ROTATION_SPEED = math.radians(30)  # radians per second

# ---------------------------------------

def closest_point_on_segment(p, a, b):
    """
    Returns the closest point on segment a-b to point p.
    p, a, b are pygame.math.Vector2.
    """
    ab = b - a
    if ab.length_squared() == 0:
        return a
    t = (p - a).dot(ab) / ab.length_squared()
    t = max(0, min(1, t))
    return a + ab * t

def wall_velocity_at_point(pt, center, omega):
    """
    Given a point pt on the rotating hexagon, compute its velocity
    due to rotation about center with angular speed omega.
    The velocity is perpendicular to (pt-center).
    """
    r = pt - center
    # In 2D, the perpendicular is given by (-r.y, r.x)
    return omega * pygame.math.Vector2(-r.y, r.x)

def hexagon_vertices(center, radius, rotation, sides=6):
    """
    Returns a list of pygame.math.Vector2 for each vertex of a regular polygon.
    'rotation' is a global rotation angle (in radians) to be added.
    """
    vertices = []
    for i in range(sides):
        angle = 2 * math.pi * i / sides + rotation
        x = center.x + radius * math.cos(angle)
        y = center.y + radius * math.sin(angle)
        vertices.append(pygame.math.Vector2(x, y))
    return vertices

class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos.copy()
        self.vel = vel.copy()
        self.radius = radius
        self.color = color

    def update(self, dt):
        # Update velocity with gravity
        self.vel += GRAVITY * dt
        # Update position
        self.pos += self.vel * dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color,
                           (int(self.pos.x), int(self.pos.y)), self.radius)

def handle_collision(ball, hex_center, hex_vertices, dt):
    """
    Check for collision between the ball and each edge of the hexagon.
    If a collision is detected, reflect the ball's velocity relative to
    the wall's moving velocity.
    """
    collided = False
    for i in range(len(hex_vertices)):
        a = hex_vertices[i]
        b = hex_vertices[(i + 1) % len(hex_vertices)]
        # Find the closest point on edge to ball center.
        cp = closest_point_on_segment(ball.pos, a, b)
        diff = ball.pos - cp
        dist = diff.length()

        if dist < ball.radius:
            # Collision detected.
            # Compute the collision normal (pointing out of the wall toward the ball)
            if dist != 0:
                normal = diff.normalize()
            else:
                # If ball center is exactly at cp, use an outward normal given by:
                # (ball_pos - hex_center) or a default direction.
                normal = (ball.pos - hex_center)
                if normal.length() == 0:
                    normal = pygame.math.Vector2(0, -1)
                else:
                    normal = normal.normalize()

            # Compute the wall (edge) velocity at the contact point:
            wall_vel = wall_velocity_at_point(cp, hex_center, ROTATION_SPEED)

            # Relative velocity of ball with respect to wall.
            rel_vel = ball.vel - wall_vel

            # Normal velocity component (dot product)
            v_n = rel_vel.dot(normal)

            # Only reflect if the ball is moving toward the wall.
            if v_n < 0:
                collided = True

                # Decompose relative velocity into normal and tangential parts.
                v_n_vec = v_n * normal
                v_t_vec = rel_vel - v_n_vec

                # Reflect the normal component with restitution
                new_v_n_vec = -RESTITUTION * v_n_vec

                # Apply friction to the tangential component
                new_v_t_vec = (1 - FRICTION_COEF) * v_t_vec

                # New relative velocity
                new_rel_vel = new_v_n_vec + new_v_t_vec

                # Convert back to lab frame by re-adding wall velocity.
                ball.vel = new_rel_vel + wall_vel

                # Reposition the ball so that it is just outside the wall.
                penetration = ball.radius - dist
                ball.pos += normal * penetration

    return collided

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ChatGPT o3 mini (medium) (28/02/2025)")
    clock = pygame.time.Clock()

    # Create a ball.
    ball = Ball(INITIAL_BALL_POS, INITIAL_BALL_VEL, BALL_RADIUS, BALL_COLOR)
    rotation = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # seconds elapsed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update hexagon rotation.
        rotation += ROTATION_SPEED * dt

        # Get current hexagon vertices.
        vertices = hexagon_vertices(HEX_CENTER, HEX_RADIUS, rotation, HEX_SIDES)

        # Update ball physics.
        ball.update(dt)

        # Handle collisions with hexagon walls.
        handle_collision(ball, HEX_CENTER, vertices, dt)

        # Fill background.
        screen.fill((30, 30, 30))

        # Draw rotating hexagon.
        points = [(int(v.x), int(v.y)) for v in vertices]
        pygame.draw.polygon(screen, HEX_COLOR, points, HEX_THICKNESS)

        # Draw ball.
        ball.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()