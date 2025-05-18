import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon"

CLOCK = pygame.time.clock()

BALL_RADIUS = 10
HEX_RADIUS = 200  # Distance from center to vertices
GRAVITY = 0.5  # Acceleration per second
ANGULAR_VELOCITY = 0.01  # Radians per second
FRICTION = 0.95  # Damping factor per second
RESTITUTION = 0.8  # Bounce factor

CENTER = (WIDTH // 2, HEIGHT // 2)
ball_x, ball_y = CENTER[0], CENTER[1] - 150  # Start above the center
ball_vx, ball_vy = 5, 0  # Initial velocity
rotation_angle = 0.0

running = True
while running:
    dt = CLOCK.tick() / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation angle
    rotation_angle += ANGULAR_VELOCITY * dt

    # Compute hexagon vertices
    vertices = []
    for i in range(6):
        angle = rotation_angle + i * (2 * math.pi /6
        x = CENTER[0] + HEX_RADIUS * math.cos angle
        y = CENTER[1] + HEX_RADIUS * math sin angle
        vertices.append( (x, y) )

    # Update ball's position and velocity
    # Apply gravity
    ball_vy += GRAVITY * dt
    # update position
    ball_x += ball_vx * dt
    ball_y += ball_vy * dt

    # apply friction (damping)
    ball_vx *== FRICTION
    ball_vy *== FRICTION

    # check for collision with edges
    collision = False
    for i in range(6):
        A = vertices[i]
        B = vertices[ (i+1) %6 ]
        ax, ay = A
        bx, by = B
        dx_edge = bx - ax
        dy_edge = by - ay

        # compute closest point on edge AB to ball's center
        ap_x = ball_x - ax
        ap_y = ball_y - ay

        dot_product = ap_x * dx_edge + ap_y * dy_edge
        length_sq = dx_edge**2 + dy_edge**2

        if length_sq ==0:
            continue

        t = dot_product / length_sq
        t = max(0.0, min(1.0, t)
        closest_x = ax + t * dx_edge
        closest_y = ay + t * dy_edge

        # compute distance squared
        dx_closest = ball_x - closest_x
        dy_closest = ball_y - closest_y
        distance_sq = dx_closest**2 + dy_closest**2

        if distance_sq < BALL_RADIUS**2:
            # compute normal vector
            normal_x = dy_edge
            normal_y = -dx_edge
            length = math.sqrt(normal_x**2 + normal_y**2
            if length ==0:
                continue
            normal_x /= length
            normal_y /= length

            # compute reflection
            v_dot_n = ball_vx * normal_x + ball_vy * normal_y
            new_vx = ball_vx - 2 * v_dot_n * normal_x
            new_vy = ball_vy - 2 * v_dot_n * normal_y

            # apply restitution
            new_vx *== RESTITUTION
            new_vy *== RESTitution

            ball_vx, ball_vy = new_vx, new_vy

            # adjust position
            penetration = math.sqrt(distance_sq) - BALL_RADIUS
            if penetration >0:
                ball_x -= normal_x * penetration
                ball_y -= normal_y * penetration

    # Draw everything
    screen.fill( (0,0,0) )

    # Draw hexagon
    pygame.draw.polygon(screen, (255,255,255, vertices, 2

    # Draw ball
    pygame.draw.circle(screen, (255,0,0, (ball_x, ball_y, BALL_RADIUS

    pygame.display.flip()

pygame.quit()