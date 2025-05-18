import pygame
import math
from pygame.math import Vector2

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Hexagon parameters
    center = Vector2(400, 300)
    hex_radius = 200
    angle = 0.0
    angular_velocity = math.radians(30)  # 30°/s

    # Ball parameters
    ball_pos = Vector2(400, 200)
    ball_vel = Vector2(200, 0)
    ball_radius = 15
    gravity = Vector2(0, 500)     # px/s²
    restitution = 0.9             # bounce energy retention
    friction = 0.05               # tangential speed loss on bounce

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds elapsed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update hexagon rotation
        angle += angular_velocity * dt

        # Apply gravity
        ball_vel += gravity * dt
        # Simple air drag
        ball_vel *= 0.999

        # Move ball
        ball_pos += ball_vel * dt

        # Compute hexagon vertices
        pts = []
        for i in range(6):
            theta = angle + i * (2 * math.pi / 6)
            x = center.x + hex_radius * math.cos(theta)
            y = center.y + hex_radius * math.sin(theta)
            pts.append(Vector2(x, y))

        # Collision with each edge
        for i in range(6):
            A = pts[i]
            B = pts[(i + 1) % 6]
            edge = B - A
            edge_len = edge.length()
            edge_dir = edge / edge_len

            # Inward normal (perp to edge)
            normal = Vector2(-edge_dir.y, edge_dir.x)
            if normal.dot(center - A) < 0:
                normal = -normal

            # Distance from ball center to edge
            to_ball = ball_pos - A
            dist = to_ball.dot(normal)
            proj = to_ball.dot(edge_dir)

            # Check collision: within edge segment and penetrating
            if dist < ball_radius and 0 < proj < edge_len:
                # Only if moving into the wall
                if ball_vel.dot(normal) < 0:
                    # Push out of wall
                    ball_pos += normal * (ball_radius - dist)

                    # Decompose velocity
                    v_n = ball_vel.dot(normal)
                    v_t = ball_vel - v_n * normal

                    # Reflect normal component with restitution
                    v_n_after = -v_n * restitution
                    # Apply tangential friction
                    v_t_after = v_t * (1 - friction)

                    ball_vel = v_n_after * normal + v_t_after

        # Draw everything
        screen.fill((30, 30, 30))
        pygame.draw.polygon(screen, (100, 200, 255),
                            [(p.x, p.y) for p in pts], width=3)
        pygame.draw.circle(screen, (255, 100, 100),
                           (int(ball_pos.x), int(ball_pos.y)),
                           ball_radius)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()