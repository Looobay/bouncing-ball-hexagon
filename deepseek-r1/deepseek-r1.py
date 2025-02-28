import pygame
import sys
import math

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Deepseek R1 (28/02/2025)")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Hexagon parameters
center = (width//2, height//2)
hex_radius = 150
rotation_speed = 0.02  # radians per frame
current_angle = 0

# Ball parameters
ball_radius = 10
ball_pos = [center[0], center[1] - 100]
ball_vel = [2.0, 0.0]
gravity = 0.2
air_friction = 0.99
restitution = 0.8
collision_friction = 0.1

def closest_point_on_segment(A, B, C):
    ax, ay = A
    bx, by = B
    cx, cy = C
    
    abx = bx - ax
    aby = by - ay
    acx = cx - ax
    acy = cy - ay
    
    t = (acx * abx + acy * aby) / max(abx**2 + aby**2, 1e-8)
    t = max(0, min(1, t))
    return (ax + t * abx, ay + t * aby)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update hexagon rotation
    current_angle += rotation_speed
    
    # Update ball physics
    ball_vel[1] += gravity
    ball_vel[0] *= air_friction
    ball_vel[1] *= air_friction
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Generate hexagon vertices
    vertices = []
    for i in range(6):
        angle = current_angle + math.radians(60 * i)
        x = center[0] + hex_radius * math.cos(angle)
        y = center[1] + hex_radius * math.sin(angle)
        vertices.append((x, y))

    # Collision detection and response
    for i in range(6):
        A = vertices[i]
        B = vertices[(i+1)%6]
        P = closest_point_on_segment(A, B, ball_pos)
        
        dx = ball_pos[0] - P[0]
        dy = ball_pos[1] - P[1]
        distance = math.hypot(dx, dy)
        
        if distance < ball_radius:
            edge_dx = B[0] - A[0]
            edge_dy = B[1] - A[1]
            
            # Calculate normal vector
            normal = (edge_dy, -edge_dx)
            length = math.hypot(*normal)
            if length == 0:
                continue
            normal = (normal[0]/length, normal[1]/length)
            
            # Calculate wall velocity at collision point
            vw_x = -rotation_speed * (P[1] - center[1])
            vw_y = rotation_speed * (P[0] - center[0])
            
            # Relative velocity
            rel_vx = ball_vel[0] - vw_x
            rel_vy = ball_vel[1] - vw_y
            
            # Calculate collision components
            dot_product = rel_vx * normal[0] + rel_vy * normal[1]
            
            if dot_product < 0:
                # Calculate collision response
                normal_component = (dot_product * normal[0], dot_product * normal[1])
                tangent_component = (rel_vx - normal_component[0], rel_vy - normal_component[1])
                
                # Apply restitution and friction
                new_normal = (-restitution * normal_component[0], -restitution * normal_component[1])
                new_tangent = ((1 - collision_friction) * tangent_component[0], 
                              (1 - collision_friction) * tangent_component[1])
                
                # Update ball velocity
                ball_vel[0] = vw_x + new_normal[0] + new_tangent[0]
                ball_vel[1] = vw_y + new_normal[1] + new_tangent[1]
            
            # Resolve penetration
            penetration = ball_radius - distance
            ball_pos[0] += normal[0] * penetration
            ball_pos[1] += normal[1] * penetration

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.polygon(screen, BLUE, vertices, 3)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.display.flip()
    clock.tick(60)