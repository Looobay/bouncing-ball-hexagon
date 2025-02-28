import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grok Beta (28/02/2025)")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.01
BALL_RADIUS = 20
HEX_RADIUS = 150
ROTATION_SPEED = 0.03

class Ball:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(2, 0)  # Initial velocity
        self.mass = 1

    def apply_gravity(self):
        self.velocity.y += GRAVITY

    def apply_friction(self):
        self.velocity.x *= 1 - FRICTION
        self.velocity.y *= 1 - FRICTION

    def move(self):
        self.pos += self.velocity
        self.apply_gravity()
        self.apply_friction()

    def bounce(self, normal):
        # Reflect velocity over the normal vector
        self.velocity = self.velocity.reflect(normal)

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.pos.x), int(self.pos.y)), BALL_RADIUS)

class Hexagon:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.angle = 0

    def update(self):
        self.angle += ROTATION_SPEED

    def get_vertices(self):
        vertices = []
        for i in range(6):
            angle = math.pi/3 * i + self.angle
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def draw(self, screen):
        vertices = self.get_vertices()
        pygame.draw.polygon(screen, WHITE, vertices, 2)

def collide_with_hexagon(ball, hexagon):
    vertices = hexagon.get_vertices()
    for i in range(len(vertices)):
        edge_start = vertices[i]
        edge_end = vertices[(i + 1) % len(vertices)]
        edge = pygame.math.Vector2(edge_end) - pygame.math.Vector2(edge_start)
        to_ball = ball.pos - pygame.math.Vector2(edge_start)
        
        # Project to_ball onto edge
        edge_length_squared = edge.length_squared()
        if edge_length_squared == 0:
            continue
        
        t = max(0, min(1, to_ball.dot(edge) / edge_length_squared))
        closest_point = pygame.math.Vector2(edge_start) + edge * t
        
        distance = (ball.pos - closest_point).length()
        
        if distance < BALL_RADIUS:
            normal = (ball.pos - closest_point).normalize()
            ball.bounce(normal)
            # Adjust position to prevent ball from going inside the hexagon
            ball.pos = closest_point + normal * BALL_RADIUS

# Initialize game objects
hexagon = Hexagon((WIDTH // 2, HEIGHT // 2), HEX_RADIUS)
ball = Ball(WIDTH // 2, HEIGHT // 4)

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    hexagon.update()
    hexagon.draw(screen)
    
    ball.move()
    collide_with_hexagon(ball, hexagon)
    ball.draw(screen)

    # Ball should bounce off the edges of the screen as well
    if ball.pos.x < BALL_RADIUS or ball.pos.x > WIDTH - BALL_RADIUS:
        ball.velocity.x *= -1
    if ball.pos.y < BALL_RADIUS:
        ball.velocity.y *= -1

    # If ball goes below screen, reset its position
    if ball.pos.y > HEIGHT + BALL_RADIUS:
        ball.pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 4)
        ball.velocity = pygame.math.Vector2(2, 0)

    pygame.display.flip()
    clock.tick(60)