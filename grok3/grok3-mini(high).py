import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5  # Downward acceleration (pixels per frame^2)
FRICTION = 0.99  # Velocity multiplier for friction
ROTATION_SPEED = 0.02  # Radians per frame for hexagon rotation
BALL_RADIUS = 10
HEX_RADIUS = 200  # Distance from center to vertex

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ball properties
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [5.0, 0.0]  # Initial velocity (x, y)

# Hexagon properties
hex_center = [WIDTH / 2, HEIGHT / 2]
hex_angle = 0.0  # Current rotation angle

def draw_hexagon(screen, center, radius, angle):
    points = []
    for i in range(6):
        point_angle = angle + i * (2 * math.pi / 6)
        x = center[0] + radius * math.cos(point_angle)
        y = center[1] + radius * math.sin(point_angle)
        points.append((x, y))
    pygame.draw.polygon(screen, (255, 255, 255), points, 1)  # Draw outline

def update_ball():
    global ball_pos, ball_vel
    
    # Apply gravity
    ball_vel[1] += GRAVITY
    
    # Apply friction
    ball_vel[0] *= FRICTION
    ball_vel[1] *= FRICTION
    
    # Update position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # Check for collisions with hexagon edges
    hex_points = [
        (
            hex_center[0] + HEX_RADIUS * math.cos(hex_angle + i * (2 * math.pi / 6)),
            hex_center[1] + HEX_RADIUS * math.sin(hex_angle + i * (2 * math.pi / 6))
        )
        for i in range(6)
    ]
    
    for i in range(6):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % 6]
        
        # Line segment from p1 to p2
        edge_vector = [p2[0] - p1[0], p2[1] - p1[1]]
        ball_to_p1 = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]
        
        # Project ball_to_p1 onto edge_vector
        projection = (
            (ball_to_p1[0] * edge_vector[0] + ball_to_p1[1] * edge_vector[1])
            / (edge_vector[0] ** 2 + edge_vector[1] ** 2)
        )
        
        closest_point = [
            p1[0] + projection * edge_vector[0],
            p1[1] + projection * edge_vector[1]
        ]
        
        distance_to_edge = math.hypot(
            ball_pos[0] - closest_point[0],
            ball_pos[1] - closest_point[1]
        )
        
        if distance_to_edge < BALL_RADIUS:
            # Collision detected
            normal = [
                ball_pos[0] - closest_point[0],
                ball_pos[1] - closest_point[1]
            ]
            normal_magnitude = math.hypot(normal[0], normal[1])
            if normal_magnitude > 0:
                normal = [normal[0] / normal_magnitude, normal[1] / normal_magnitude]
            
            # Reflect velocity
            dot_product = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
            ball_vel[0] -= 2 * dot_product * normal[0]
            ball_vel[1] -= 2 * dot_product * normal[1]
            
            # Move ball out of collision
            overlap = BALL_RADIUS - distance_to_edge
            ball_pos[0] += normal[0] * overlap
            ball_pos[1] += normal[1] * overlap

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update hexagon rotation
        global hex_angle
        hex_angle += ROTATION_SPEED
        hex_angle %= 2 * math.pi  # Keep angle within 0-2π
        
        update_ball()
        
        screen.fill((0, 0, 0))  # Clear screen
        draw_hexagon(screen, hex_center, HEX_RADIUS, hex_angle)
        pygame.draw.circle(screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()