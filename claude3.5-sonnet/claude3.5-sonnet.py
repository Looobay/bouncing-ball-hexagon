import pygame
import math
import numpy as np
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.98
BALL_RADIUS = 10
HEX_RADIUS = 150
ROTATION_SPEED = 0.02

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Claude 3.5 - Sonnet (28/02/2025)")
clock = pygame.time.Clock()


class Ball:
    def __init__(self, x: float, y: float):
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([0.0, 0.0])

    def update(self):
        # Apply gravity
        self.vel[1] += GRAVITY
        # Apply velocity
        self.pos += self.vel
        # Apply friction
        self.vel *= FRICTION

    def draw(self, surface):
        pygame.draw.circle(
            surface, RED, (int(self.pos[0]), int(self.pos[1])), BALL_RADIUS
        )


def get_hexagon_points(angle: float) -> List[np.ndarray]:
    points = []
    center = np.array([WIDTH / 2, HEIGHT / 2])
    for i in range(6):
        theta = angle + i * math.pi / 3
        x = center[0] + HEX_RADIUS * math.cos(theta)
        y = center[1] + HEX_RADIUS * math.sin(theta)
        points.append(np.array([x, y]))
    return points


def line_segment_normal(p1: np.ndarray, p2: np.ndarray) -> np.ndarray:
    direction = p2 - p1
    normal = np.array([-direction[1], direction[0]])
    return normal / np.linalg.norm(normal)


def check_collision(
    ball: Ball, p1: np.ndarray, p2: np.ndarray
) -> Tuple[bool, np.ndarray]:
    # Get the normal vector of the line segment
    normal = line_segment_normal(p1, p2)

    # Vector from p1 to ball
    to_ball = ball.pos - p1

    # Project to_ball onto the normal
    distance = np.dot(to_ball, normal)

    if abs(distance) <= BALL_RADIUS:
        # Check if the ball is between the endpoints
        line_vec = p2 - p1
        line_length = np.linalg.norm(line_vec)
        line_unit = line_vec / line_length
        proj_length = np.dot(to_ball, line_unit)

        if 0 <= proj_length <= line_length:
            return True, normal

    return False, np.array([0, 0])


def main():
    ball = Ball(WIDTH / 2, HEIGHT / 2)
    angle = 0

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        angle += ROTATION_SPEED
        hex_points = get_hexagon_points(angle)
        ball.update()

        # Check collisions with all hexagon sides
        for i in range(6):
            p1 = hex_points[i]
            p2 = hex_points[(i + 1) % 6]
            collision, normal = check_collision(ball, p1, p2)

            if collision:
                # Reflect velocity vector off the wall
                ball.vel = (
                    ball.vel
                    - 2 * np.dot(ball.vel, normal) * normal
                    * FRICTION
                )
                # Push ball out of the wall
                ball.pos += normal * (BALL_RADIUS - abs(np.dot(ball.pos - p1, normal)))

        # Draw
        screen.fill(BLACK)

        # Draw hexagon
        pygame.draw.polygon(screen, WHITE, hex_points, 2)

        # Draw ball
        ball.draw(screen)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
