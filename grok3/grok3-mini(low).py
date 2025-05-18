import pygame
import math

# Constants
WIDTH = 800  # Screen width
HEIGHT = 600  # Screen height
GRAVITY = 0.5  # Downward acceleration (pixels per frame^2)
FRICTION = 0.99  # Velocity damping factor (multiplier per frame)
ROTATION_SPEED = 0.01  # Rotation speed in radians per frame
HEX_RADIUS = 200  # Distance from hexagon center to vertex
BALL_RADIUS = 10  # Ball radius
HEX_CENTER = [WIDTH / 2, HEIGHT / 2]  # Hexagon center

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ball properties
ball_pos = [HEX_CENTER[0], HEX_CENTER[1] / 2]  # Start ball near top
ball_vel = [5.0, 0.0]  # Initial velocity (e.g., some horizontal speed)

# Hexagon properties
hex_angle = 0.0  # Current rotation angle

def draw_hexagon(center, radius, angle):
    points = []
    for i in range(6):
        point_angle = angle + i * (2 * math.pi / 6)
        x = center[0] + radius * math.cos(point_angle)
        y = center[1] + radius * math.sin(point_angle)
        points.append((x, y))
    pygame.draw.polygon(screen, (255, 255, 255), points, 1)  # Draw outline

def update_ball(hex_points):
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
    for i in range(6):
        p1 = hex_points[i]
        p2 = hex_points[(i + 1) % 6]  # Next point, wrapping around
        # Get closest point on line segment p1-p2 to ball_pos
        line_vec = [p2[0] - p1[0], p2[1] - p1[1]]
        point_to_p1 = [ball_pos[0] - p1[0], ball_pos[1] - p1[1]]
        
        line_len = math.hypot(line_vec[0], line_vec[1])
        if line_len == 0:
            continue  # Degenerate case
        line_unit = [line_vec[0] / line_len, line_vec[1] / line_len]
        
        proj = point_to_p1[0] * line_unit[0] + point_to_p1[1] * line_unit[1]
        proj = max(0, min(1, proj / line_len))  # Clamp to segment
        closest_point = [
            p1[0] + proj * line_unit[0] * line_len,
            p1[1] + proj * line_unit[1] * line_len
        ]
        
        distance = math.hypot(
            ball_pos[0] - closest_point[0],
            ball_pos[1] - closest_point[1]
        )
        
        if distance < BALL_RADIUS:  # Collision detected
            # Get normal vector (perpendicular to line)
            normal = [-line_unit[1], line_unit[0]]  # 90 degrees rotated
            norm_len = math.hypot(normal[0], normal[1])
            normal = [normal[0] / norm_len, normal[1] / norm_len]
            
            # Reflect velocity: new_vel = vel - 2 * (vel • normal) * normal
            dot_product = ball_vel[0] * normal[0] + ball_vel[1] * normal[1]
            ball_vel[0] -= 2 * dot_product * normal[0]
            ball_vel[1] -= 2 * dot_product * normal[1]
            
            # Move ball out of collision to prevent sticking
            overlap = BALL_RADIUS - distance
            ball_pos[0] += normal[0] * overlap
            ball_pos[1] += normal[1] * overlap

def main():
    global hex_angle
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update hexagon angle
        hex_angle += ROTATION_SPEED
        
        # Get current hexagon points
        hex_points = []
        for i in range(6):
            point_angle = hex_angle + i * (2 * math.pi / 6)
            x = HEX_CENTER[0] + HEX_RADIUS * math.cos(point_angle)
            y = HEX_CENTER[1] + HEX_RADIUS * math.sin(point_angle)
            hex_points.append((x, y))
        
        # Update ball physics
        update_ball(hex_points)
        
        # Draw everything
        screen.fill((0, 0, 0))  # Black background
        draw_hexagon(HEX_CENTER, HEX_RADIUS, hex_angle)
        pygame.draw.circle(
            screen, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS
        )
        
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()