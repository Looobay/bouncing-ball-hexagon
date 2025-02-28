import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
HEXAGON_COLOR = (255, 255, 255)
BALL_COLOR = (255, 0, 0)
BALL_RADIUS = 15
HEXAGON_RADIUS = 200
GRAVITY = 0.2
FRICTION = 0.99
ROTATION_SPEED = 0.01
RESTITUTION = 0.8  # Bounciness factor

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Claude 3.7 - Sonnet - Reasoning (medium) (28/02/2025)")
clock = pygame.time.Clock()

# Center of the screen
center = (WIDTH // 2, HEIGHT // 2)

# Create the hexagon vertices
def create_hexagon(center, radius):
    vertices = []
    for i in range(6):
        angle = math.pi / 3 * i
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

# Rotate vertices around a center point
def rotate_vertices(vertices, center, angle):
    rotated = []
    for x, y in vertices:
        dx = x - center[0]
        dy = y - center[1]
        rx = dx * math.cos(angle) - dy * math.sin(angle)
        ry = dx * math.sin(angle) + dy * math.cos(angle)
        rotated.append((rx + center[0], ry + center[1]))
    return rotated

# Get the closest point on a line segment to a point
def closest_point_on_line(point, line_start, line_end):
    line_vec = np.array([line_end[0] - line_start[0], line_end[1] - line_start[1]])
    point_vec = np.array([point[0] - line_start[0], point[1] - line_start[1]])
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    
    # Calculate projection of point onto line vector
    scalar_projection = np.dot(point_vec, line_unitvec)
    scalar_projection = max(0, min(line_len, scalar_projection))  # Clamp to line segment
    
    # Get the closest point
    closest_point = np.array([
        line_start[0] + scalar_projection * line_unitvec[0],
        line_start[1] + scalar_projection * line_unitvec[1]
    ])
    
    return closest_point

# Check if ball collides with any hexagon side and handle bounce
def handle_collision(ball_pos, ball_vel, hexagon_vertices):
    collided = False
    new_vel = np.array(ball_vel)
    
    for i in range(6):
        # Get current side
        start = hexagon_vertices[i]
        end = hexagon_vertices[(i+1) % 6]
        
        # Find closest point on the line segment to the ball
        closest = closest_point_on_line(ball_pos, start, end)
        
        # Calculate distance between the ball and the closest point
        distance = np.linalg.norm(np.array(ball_pos) - closest)
        
        if distance <= BALL_RADIUS:
            # Calculate the wall normal (perpendicular to the side)
            wall_vec = np.array([end[0] - start[0], end[1] - start[1]])
            wall_normal = np.array([-wall_vec[1], wall_vec[0]])  # Perpendicular
            wall_normal = wall_normal / np.linalg.norm(wall_normal)  # Normalize
            
            # Make sure the normal points toward the ball
            if np.dot(wall_normal, np.array(ball_pos) - closest) < 0:
                wall_normal = -wall_normal
                
            # Calculate relative velocity (include hexagon rotation effect at collision point)
            # For simplicity, we'll just use the ball's velocity for now
            relative_vel = np.array(ball_vel)
            
            # Check if ball is moving toward the wall
            normal_velocity = np.dot(relative_vel, wall_normal)
            if normal_velocity < 0:
                # Calculate impulse
                impulse = -normal_velocity * (1 + RESTITUTION)
                
                # Apply impulse along normal direction
                new_vel = new_vel + impulse * wall_normal
                
                # Move ball outside the wall to prevent sticking
                penetration = BALL_RADIUS - distance
                ball_pos[0] += wall_normal[0] * penetration
                ball_pos[1] += wall_normal[1] * penetration
                
                collided = True
    
    return new_vel.tolist(), collided

# Main game variables
hexagon_vertices = create_hexagon(center, HEXAGON_RADIUS)
rotation_angle = 0
ball_pos = [center[0], center[1] - 100]  # Start ball above center
ball_vel = [1.0, 0.5]  # Initial velocity

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Rotate hexagon
    rotation_angle += ROTATION_SPEED
    rotated_hexagon = rotate_vertices(hexagon_vertices, center, rotation_angle)
    
    # Update ball position with gravity
    ball_vel[0] *= FRICTION  # Apply horizontal friction
    ball_vel[1] += GRAVITY   # Apply gravity
    ball_vel[1] *= FRICTION  # Apply vertical friction
    
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Check for collision and handle bounce
    ball_vel, collided = handle_collision(ball_pos, ball_vel, rotated_hexagon)
    
    # Drawing
    screen.fill(BACKGROUND_COLOR)
    
    # Draw hexagon
    pygame.draw.polygon(screen, HEXAGON_COLOR, rotated_hexagon, width=2)
    
    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
