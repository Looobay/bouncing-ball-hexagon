import pygame
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grok 3 (28/02/2025)")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Ball properties
ball_radius = 20
ball_pos = np.array([WIDTH/2, HEIGHT/2], dtype=float)
ball_vel = np.array([5.0, -5.0], dtype=float)
gravity = np.array([0.0, 0.2])
friction = 0.99

# Hexagon properties
hex_radius = 300
hex_center = (WIDTH/2, HEIGHT/2)
rotation_speed = 0.02  # radians per frame
hex_angle = 0

def get_hexagon_vertices(center, radius, angle):
    """Calculate vertices of a rotating hexagon"""
    vertices = []
    for i in range(6):
        vertex_angle = angle + i * math.pi / 3
        x = center[0] + radius * math.cos(vertex_angle)
        y = center[1] + radius * math.sin(vertex_angle)
        vertices.append((x, y))
    return vertices

def line_intersection(p1, p2, p3, p4):
    """Find intersection point between two line segments"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None
    
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
    
    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    return None

def reflect_velocity(vel, normal):
    """Calculate reflection of velocity vector off a surface"""
    normal = np.array(normal) / np.linalg.norm(normal)
    return vel - 2 * np.dot(vel, normal) * normal

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update ball position
    ball_vel += gravity
    ball_vel *= friction
    next_pos = ball_pos + ball_vel
    
    # Get hexagon vertices
    vertices = get_hexagon_vertices(hex_center, hex_radius, hex_angle)
    
    # Check collisions with hexagon walls
    for i in range(6):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % 6]
        
        # Check if ball crosses this wall
        intersection = line_intersection(
            ball_pos, next_pos,
            v1, v2
        )
        
        if intersection:
            # Calculate wall normal (perpendicular to wall)
            wall_vec = np.array([v2[0] - v1[0], v2[1] - v1[1]])
            normal = np.array([-wall_vec[1], wall_vec[0]])
            
            # Reflect velocity
            ball_vel = reflect_velocity(ball_vel, normal) * 0.8  # 0.8 is bounce dampening
            ball_pos = np.array(intersection)
            break
    else:
        ball_pos = next_pos
    
    # Update hexagon rotation
    hex_angle += rotation_speed
    
    # Clear screen
    screen.fill(BLACK)
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, ball_pos.astype(int), ball_radius)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()