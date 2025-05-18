import math
import pygame

# ----- Configuration Constants -----
WIDTH, HEIGHT = 800, 600         # Window dimensions
FPS = 60                         # Frames per second

GRAVITY = 500                    # Acceleration due to gravity (pixels/s^2)
FRICTION = 0.99                  # Damping factor for ball velocity (air friction)

BALL_RADIUS = 10                 # Radius of the ball (pixels)
BALL_RESTITUTION = 0.9           # Bounce coefficient (1 = elastic bounce)

# Hexagon parameters
HEX_CENTER = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
HEX_RADIUS = 250                 # Distance from center to vertex
HEX_ANGULAR_SPEED = 0.5          # Angular speed in radians per second

# ----- Helper Functions -----

def get_hexagon_vertices(center, radius, angle):
    """
    Compute the six vertices of a regular hexagon centered at `center`
    with circumradius `radius`. The hexagon is rotated by the given `angle`
    (in radians).
    """
    vertices = []
    for i in range(6):
        theta = angle + i * (2 * math.pi / 6)
        x = center.x + radius * math.cos(theta)
        y = center.y + radius * math.sin(theta)
        vertices.append(pygame.math.Vector2(x, y))
    return vertices


def reflect_ball(ball_velocity, wall_velocity, n):
    """
    Reflect the ball’s velocity off a wall.
    
    The wall is moving with velocity `wall_velocity`. Let
    \(\vec{v}_{\text{rel}} = \vec{v}_{\text{ball}} - \vec{v}_{\text{wall}}\).
    Decompose this relative velocity into tangent and normal components,
    and reflect the normal one with restitution \(e\):
    
        v_new_rel = v_rel_tan - e * v_rel_n
    
    Then return:
    
        v_ball_new = wall_velocity + v_new_rel
    """
    rel = ball_velocity - wall_velocity
    # Normal component: (v_rel dot n)*n
    v_rel_n = rel.dot(n) * n
    # Tangential component: v_rel - v_rel_n
    v_rel_t = rel - v_rel_n
    # Reflect the normal component (note the minus sign) and apply restitution
    new_rel = v_rel_t - BALL_RESTITUTION * v_rel_n
    return wall_velocity + new_rel


def check_collision(ball_pos, ball_vel, ball_radius, hex_vertices,
                    hex_center, hex_angular_speed):
    """
    Check collision of the ball (a circle) with each edge of the hexagon.
    For each edge (or vertex) we compute the closest point to the ball center.
    If the distance is less than the ball's radius the ball is repositioned
    and its velocity is updated. The wall's local velocity is computed from
    the hexagon's angular speed.
    """
    for i in range(len(hex_vertices)):
        A = hex_vertices[i]
        B = hex_vertices[(i + 1) % len(hex_vertices)]
        AB = B - A
        # Vector from A to ball center
        AC = ball_pos - A
        # Projection factor: t = (AC . AB) / |AB|^2, clamped to [0, 1]
        if AB.length_squared() != 0:
            t = AC.dot(AB) / AB.length_squared()
        else:
            t = 0
        t = max(0, min(1, t))
        # Find the closest point on the line segment AB
        closest = A + t * AB
        # Compute the distance from the ball center to the closest point
        diff = ball_pos - closest
        dist = diff.length()
        if dist < ball_radius:
            # A collision has occurred!
            # Compute collision normal. If diff is nearly zero, choose a fallback.
            if diff.length() == 0:
                midpoint = (A + B) * 0.5
                diff = ball_pos - midpoint
                if diff.length() == 0:
                    diff = pygame.math.Vector2(1, 0)
                else:
                    diff = diff.normalize()
            else:
                diff = diff.normalize()
            n = diff  # collision normal (points from wall toward ball)
            penetration = ball_radius - dist
            # Correct the ball's position so it is not overlapping.
            ball_pos += n * penetration

            # Compute the wall's velocity at the contact point.
            # For a rotating hexagon about its center, any point's velocity is:
            # v_wall = ω × (contact_point - hex_center),
            # which in 2D is given by:
            wall_vel = pygame.math.Vector2(-hex_angular_speed * (closest.y - hex_center.y),
                                             hex_angular_speed * (closest.x - hex_center.x))
            # Only reflect if the ball is moving toward the wall.
            rel_vel = ball_vel - wall_vel
            if rel_vel.dot(n) < 0:
                ball_vel = reflect_ball(ball_vel, wall_vel, n)
    return ball_pos, ball_vel


# ----- Main Function -----

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
    clock = pygame.time.Clock()

    # Start with the ball at the center and a small initial velocity.
    ball_pos = pygame.math.Vector2(HEX_CENTER)
    ball_vel = pygame.math.Vector2(150, -200)
    
    # Initial hexagon rotation angle (in radians)
    hex_angle = 0.0

    running = True
    while running:
        # dt: time elapsed in seconds since the last frame.
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ----- Update Ball Physics -----
        # Apply gravity (vertical acceleration)
        ball_vel.y += GRAVITY * dt
        # Update the ball's position
        ball_pos += ball_vel * dt
        # Apply friction (damping the velocity slightly)
        ball_vel *= FRICTION

        # ----- Update Hexagon Rotation -----
        hex_angle += HEX_ANGULAR_SPEED * dt
        hex_vertices = get_hexagon_vertices(HEX_CENTER, HEX_RADIUS, hex_angle)

        # ----- Check and Resolve Collisions -----
        ball_pos, ball_vel = check_collision(
            ball_pos, ball_vel, BALL_RADIUS, hex_vertices, HEX_CENTER,
            HEX_ANGULAR_SPEED
        )

        # ----- Rendering -----
        screen.fill((30, 30, 30))  # Dark background

        # Draw the hexagon (as a polygon outline)
        hex_points = [(v.x, v.y) for v in hex_vertices]
        pygame.draw.polygon(screen, (200, 200, 200), hex_points, 3)

        # Draw the ball
        pygame.draw.circle(screen, (255, 100, 100),
                           (int(ball_pos.x), int(ball_pos.y)), BALL_RADIUS)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()