import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.98
ELASTICITY = 0.8

class Ball:
    def __init__(self, x, y, radius=15):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.radius = radius
        self.color = RED
    
    def update(self):
        # Apply gravity
        self.velocity[1] += GRAVITY
        
        # Apply friction
        self.velocity *= FRICTION
        
        # Update position
        self.position += self.velocity
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.astype(int), self.radius)

class Hexagon:
    def __init__(self, center_x, center_y, radius=200):
        self.center = np.array([center_x, center_y])
        self.radius = radius
        self.angle = 0
        self.rotation_speed = 0.01
        self.color = BLUE
        self.vertices = self.calculate_vertices()
    
    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle = self.angle + i * (2 * math.pi / 6)
            x = self.center[0] + self.radius * math.cos(angle)
            y = self.center[1] + self.radius * math.sin(angle)
            vertices.append(np.array([x, y]))
        return vertices
    
    def update(self):
        self.angle += self.rotation_speed
        self.vertices = self.calculate_vertices()
    
    def draw(self, screen):
        # Draw hexagon
        pygame.draw.polygon(screen, self.color, self.vertices, 2)

def check_collision(ball, hexagon):
    # Get the vertices of the hexagon
    vertices = hexagon.vertices
    
    # Check collision with each wall of the hexagon
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i+1) % len(vertices)]
        
        # Line segment from v1 to v2
        wall_vector = v2 - v1
        wall_length = np.linalg.norm(wall_vector)
        wall_unit = wall_vector / wall_length
        
        # Vector from v1 to ball center
        to_ball = ball.position - v1
        
        # Project to_ball onto the wall vector to find the closest point
        projection_length = np.dot(to_ball, wall_unit)
        projection_length = max(0, min(wall_length, projection_length))
        
        # Calculate the closest point on the wall
        closest_point = v1 + wall_unit * projection_length
        
        # Vector from closest point to ball center
        to_ball_center = ball.position - closest_point
        distance = np.linalg.norm(to_ball_center)
        
        # Check if the ball is colliding with the wall
        if distance <= ball.radius:
            # Calculate reflection
            if distance > 0:  # Avoid division by zero
                normal = to_ball_center / distance
            else:
                normal = np.array([0, -1])  # Default normal if distance is zero
            
            # Move ball outside the wall
            overlap = ball.radius - distance
            ball.position += normal * overlap
            
            # Reflect velocity with elasticity
            ball.velocity = ball.velocity - 2 * np.dot(ball.velocity, normal) * normal
            ball.velocity *= ELASTICITY
            
            return True
    
    return False

def main():
    # Setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Claude 3.7 - Sonnet - Reasoning (low) (28/02/2025)")
    clock = pygame.time.Clock()
    
    # Create objects
    ball = Ball(WIDTH // 2, HEIGHT // 3)
    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2)
    
    # Initial impulse to make things interesting
    ball.velocity = np.array([3.0, -2.0])
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update objects
        hexagon.update()
        ball.update()
        
        # Check collisions
        check_collision(ball, hexagon)
        
        # Drawing
        screen.fill(BLACK)
        hexagon.draw(screen)
        ball.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()