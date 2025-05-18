import math
import pygame
import random

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (150, 150, 150)

# --- Classes ---
class Ball:

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.2
        self.friction = 0.02
        self.restitution = 0.7  # Bounciness (0 to 1)

    def update(self, hexagon_vertices, rotation_angle):
        # Apply gravity
        self.velocity_y += self.gravity

        # Apply friction
        self.velocity_x *= 1 - self.friction
        self.velocity_y *= 1 - self.friction

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Collision with hexagon walls
        for i in range(6):
            p1 = hexagon_vertices[i]
            p2 = hexagon_vertices[(i + 1) % 6]

            # Rotate points to account for hexagon rotation
            rotated_p1 = self.rotate_point(p1, (WIDTH // 2, HEIGHT // 2), rotation_angle)
            rotated_p2 = self.rotate_point(p2, (WIDTH // 2, HEIGHT // 2), rotation_angle)

            # Calculate the line segment's normal
            line_x = rotated_p2[0] - rotated_p1[0]
            line_y = rotated_p2[1] - rotated_p1[1]
            normal_x = -line_y
            normal_y = line_x
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            normal_x /= normal_length
            normal_y /= normal_length

            # Calculate distance from the ball's center to the line
            ball_to_p1_x = self.x - rotated_p1[0]
            ball_to_p1_y = self.y - rotated_p1[1]
            distance = ball_to_p1_x * normal_x + ball_to_p1_y * normal_y

            # Check for collision
            if (
                abs(distance) <= self.radius
                and (
                    (ball_to_p1_x * line_x + ball_to_p1_y * line_y) >= 0
                    and ((self.x - rotated_p2[0]) * line_x + (self.y - rotated_p2[1]) * line_y) <= 0
                )
            ):
                # Calculate the relative velocity
                relative_velocity_x = self.velocity_x
                relative_velocity_y = self.velocity_y

                # Calculate the dot product of the relative velocity and the normal
                dot_product = relative_velocity_x * normal_x + relative_velocity_y * normal_y

                # Reflect the velocity
                self.velocity_x -= 2 * dot_product * normal_x * self.restitution
                self.velocity_y -= 2 * dot_product * normal_y * self.restitution

                # Move the ball out of the wall to prevent sticking
                overlap = self.radius - abs(distance)
                self.x += overlap * normal_x
                self.y += overlap * normal_y

        # Keep ball within bounds (for demonstration, can be removed if hexagon is always the boundary)
        if self.x - self.radius < 0:
            self.x = self.radius
            self.velocity_x *= -self.restitution
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.velocity_x *= -self.restitution
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity_y *= -self.restitution
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.velocity_y *= -self.restitution

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def rotate_point(self, point, origin, angle):
        """Rotates a point around an origin by a given angle (in degrees)."""
        angle_rad = math.radians(angle)
        x, y = point
        ox, oy = origin
        rotated_x = ox + (x - ox) * math.cos(angle_rad) - (y - oy) * math.sin(angle_rad)
        rotated_y = oy + (x - ox) * math.sin(angle_rad) + (y - oy) * math.cos(angle_rad)
        return (rotated_x, rotated_y)


class Hexagon:

    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.rotation_speed = 1  # Degrees per frame
        self.rotation_angle = 0

    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle_deg = 60 * i + self.rotation_angle
            angle_rad = math.radians(angle_deg)
            vertex_x = self.x + self.radius * math.cos(angle_rad)
            vertex_y = self.y + self.radius * math.sin(angle_rad)
            vertices.append((vertex_x, vertex_y))
        return vertices

    def update(self):
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360

    def draw(self, screen):
        vertices = self.get_vertices()
        pygame.draw.polygon(screen, self.color, vertices, 2)  # 2 for line thickness


# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gemini 2.0 Flash Lite (28/02/2025)")
clock = pygame.time.Clock()

# --- Game Objects ---
ball = Ball(WIDTH // 2, HEIGHT // 2, 15, BLUE)
hexagon = Hexagon(WIDTH // 2, HEIGHT // 2, 150, RED)

# --- Main Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Give the ball an initial velocity on mouse click
            mouse_x, mouse_y = event.pos
            dx = mouse_x - ball.x
            dy = mouse_y - ball.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:  # Avoid division by zero
                force = 10  # Adjust for desired force
                ball.velocity_x = dx / distance * force
                ball.velocity_y = dy / distance * force

    # --- Update ---
    hexagon.update()
    hexagon_vertices = hexagon.get_vertices()
    ball.update(hexagon_vertices, hexagon.rotation_angle)

    # --- Draw ---
    screen.fill(BLACK)
    hexagon.draw(screen)
    ball.draw(screen)
    pygame.display.flip()

    # --- Control Frame Rate ---
    clock.tick(FPS)

# --- Quit ---
pygame.quit()
