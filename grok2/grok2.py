import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grok 2 (28/02/2025)")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Hexagon properties
HEX_RADIUS = 200
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
ROTATION_SPEED = 0.01  # radians per frame

# Ball properties
BALL_RADIUS = 20
BALL_MASS = 1
GRAVITY = 0.1
FRICTION = 0.99

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        # Apply gravity
        self.vy += GRAVITY

        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

        # Update position
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), BALL_RADIUS)

def create_hexagon(center, radius):
    points = []
    for i in range(6):
        angle = 2 * math.pi / 6 * i
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points

def rotate_point(point, angle, center):
    x, y = point
    cx, cy = center
    new_x = cx + (x - cx) * math.cos(angle) - (y - cy) * math.sin(angle)
    new_y = cy + (x - cx) * math.sin(angle) + (y - cy) * math.cos(angle)
    return (new_x, new_y)

def check_collision(ball, hexagon, rotation):
    for i in range(6):
        p1 = rotate_point(hexagon[i], rotation, HEX_CENTER)
        p2 = rotate_point(hexagon[(i + 1) % 6], rotation, HEX_CENTER)
        
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = abs(dy * (ball.x - p1[0]) - dx * (ball.y - p1[1])) / math.sqrt(dx**2 + dy**2)
        
        if dist < BALL_RADIUS:
            # Calculate normal vector
            nx = dy
            ny = -dx
            n_mag = math.sqrt(nx**2 + ny**2)
            nx /= n_mag
            ny /= n_mag
            
            # Calculate dot product
            dot = ball.vx * nx + ball.vy * ny
            
            # Reflect velocity
            ball.vx -= 2 * dot * nx
            ball.vy -= 2 * dot * ny
            
            # Move ball out of collision
            ball.x += nx * (BALL_RADIUS - dist)
            ball.y += ny * (BALL_RADIUS - dist)

# Create ball and hexagon
ball = Ball(WIDTH // 2, HEIGHT // 2 - 100)
hexagon = create_hexagon(HEX_CENTER, HEX_RADIUS)

# Main game loop
clock = pygame.time.Clock()
rotation = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball physics
    ball.update()

    # Check for collisions
    check_collision(ball, hexagon, rotation)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the hexagon
    rotated_hex = [rotate_point(p, rotation, HEX_CENTER) for p in hexagon]
    pygame.draw.polygon(screen, WHITE, rotated_hex, 2)

    # Draw the ball
    ball.draw()

    # Update rotation
    rotation += ROTATION_SPEED

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()