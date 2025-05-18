import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BALL_COLOR = (255, 100, 100)
HEXAGON_COLOR = (100, 255, 100)

# Time step
FPS = 60
clock = pygame.time.Clock()

# Ball properties
ball_radius = 10
ball_pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
ball_vel = pygame.Vector2(200, -50)  # initial velocity
gravity = pygame.Vector2(0, 400)     # pixels per second^2
# A simple friction coefficient, applied when ball touches the wall
friction = 0.8

# Hexagon properties
hex_center = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
hex_radius = 200  # distance from center to the vertices
hex_angle = 0     # start rotation angle
hex_rotation_speed = 0.5  # radians per second

def get_hexagon_vertices(center, radius, angle):
    """Return list of vertices for a hexagon rotated by angle (in radians)."""
    vertices = []
    for i in range(6):
        theta = angle + i * (2 * math.pi / 6)
        x = center.x + radius * math.cos(theta)
        y = center.y + radius * math.sin(theta)
        vertices.append(pygame.Vector2(x, y))
    return vertices

def point_line_distance(point, line_start, line_end):
    """
    Compute the shortest distance between a point and a line segment.
    Returns (distance, closest point on segment)
    """
    line = line_end - line_start
    if line.length_squared() == 0:
        return (point.distance_to(line_start), line_start)
    # projection factor of point onto line
    t = max(0, min(1, (point - line_start).dot(line) / line.length_squared()))
    closest = line_start + t * line
    return (point.distance_to(closest), closest)

def reflect_vector(velocity, normal):
    """
    Reflect velocity vector based on collision with a surface defined by normal.
    The reflection formula is: v' = v - 2*(v dot n)*n
    """
    return velocity - 2 * velocity.dot(normal) * normal

def main():
    global ball_pos, ball_vel, hex_angle

    dt = 1 / FPS  # Time step (in seconds)

    running = True

    while running:
        clock.tick(FPS)
        # ----- Event Handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ----- Physics Updates -----

        # Update rotation of hexagon
        hex_angle += hex_rotation_speed * dt
        vertices = get_hexagon_vertices(hex_center, hex_radius, hex_angle)

        # Apply gravity to ball velocity
        ball_vel += gravity * dt

        # Update ball position
        ball_pos += ball_vel * dt

        # Check collision with hexagon walls
        # Iterate over the edges. If the distance from the ball to an edge is less than 
        # the ball's radius, and the ball is moving toward the line; we reflect the velocity.
        for i in range(len(vertices)):
            v_start = vertices[i]
            v_end = vertices[(i + 1) % len(vertices)]
            distance, closest = point_line_distance(ball_pos, v_start, v_end)
            if distance < ball_radius:
                # Determine edge vector and normal
                edge_vec = v_end - v_start
                # Normalize perpendicular (rotate edge vector 90 degrees)
                normal = pygame.Vector2(-edge_vec.y, edge_vec.x).normalize()
                # Ensure the ball is on the correct side of the line (i.e. heading into the wall)
                if (ball_vel.dot(normal) < 0):
                    # Reflect the ball velocity
                    ball_vel = reflect_vector(ball_vel, normal)
                    # Apply friction (damp the velocity a bit)
                    ball_vel *= friction

                    # Push the ball out of collision slightly
                    overlap = ball_radius - distance
                    ball_pos += normal * overlap

        # Also check for collisions with the window edges so that the ball doesn't fly off-screen.
        # Left/Right wall
        if ball_pos.x - ball_radius < 0:
            ball_pos.x = ball_radius
            ball_vel.x = -ball_vel.x * friction
        if ball_pos.x + ball_radius > WIDTH:
            ball_pos.x = WIDTH - ball_radius
            ball_vel.x = -ball_vel.x * friction
        # Top/Bottom wall
        if ball_pos.y - ball_radius < 0:
            ball_pos.y = ball_radius
            ball_vel.y = -ball_vel.y * friction
        if ball_pos.y + ball_radius > HEIGHT:
            ball_pos.y = HEIGHT - ball_radius
            ball_vel.y = -ball_vel.y * friction

        # ----- Drawing -----
        screen.fill(BLACK)

        # Draw hexagon
        pygame.draw.polygon(screen, HEXAGON_COLOR, [v.xy for v in vertices], 3)

        # Draw ball
        pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos.x), int(ball_pos.y)),
                           ball_radius)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()