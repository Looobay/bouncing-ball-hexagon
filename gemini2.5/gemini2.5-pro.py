import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon (Simplified)")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

# Hexagon parameters
center_x = screen_width // 2
center_y = screen_height // 2
hexagon_size = 150
hexagon_angle = 0  # Initial rotation angle
rotation_speed = 0.5  # Degrees per frame

# Ball parameters
ball_radius = 10
ball_x = center_x
ball_y = center_y - hexagon_size + ball_radius * 2 # Start above the center
ball_vel_x = 5
ball_vel_y = 0
gravity = 0.2
friction_factor = 0.95 # Multiplier for velocity reduction on bounce

# Function to get hexagon vertices based on angle
def get_hexagon_vertices(center_x, center_y, size, angle_degrees):
    vertices = []
    angle_radians = math.radians(angle_degrees)
    for i in range(6):
        x = center_x + size * math.cos(angle_radians + math.radians(i * 60))
        y = center_y + size * math.sin(angle_radians + math.radians(i * 60))
        vertices.append((x, y))
    return vertices

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ball position
    ball_vel_y += gravity
    ball_x += ball_vel_x
    ball_y += ball_vel_y

    # Get current hexagon vertices
    hexagon_vertices = get_hexagon_vertices(center_x, center_y, hexagon_size, hexagon_angle)

    # Simplified collision detection and response (needs significant improvement for realism)
    # This is a very basic check and doesn't handle collisions with rotating walls accurately
    for i in range(6):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % 6]

        # Basic bounding box check (very rough)
        if min(p1[0], p2[0]) < ball_x < max(p1[0], p2[0]) and min(p1[1], p2[1]) < ball_y < max(p1[1], p2[1]):
             # Simple reflection (doesn't consider wall angle or velocity)
             # Needs proper vector math for realistic bounce
             # For a vertical line, reflect x velocity
             if abs(p1[0] - p2[0]) < 0.1: # Approximately vertical
                 ball_vel_x *= -1 * friction_factor
             # For a horizontal line, reflect y velocity
             elif abs(p1[1] - p2[1]) < 0.1: # Approximately horizontal
                  ball_vel_y *= -1 * friction_factor
             # For angled lines, this simple reflection is inaccurate
             else:
                 # This is a very rough approximation for angled walls
                 ball_vel_x *= -1 * friction_factor
                 ball_vel_y *= -1 * friction_factor

             # Move the ball slightly away from the wall to prevent sticking
             # This is a hacky solution, proper collision response handles this
             if ball_vel_x > 0:
                 ball_x += 5
             else:
                 ball_x -= 5
             if ball_vel_y > 0:
                 ball_y += 5
             else:
                 ball_y -= 5


    # Check for collision with screen edges (as a fallback/initial test)
    # This part is less relevant for bouncing inside a hexagon, but kept for basic testing
    if ball_x - ball_radius < 0 or ball_x + ball_radius > screen_width:
        ball_vel_x *= -1 * friction_factor
    if ball_y - ball_radius < 0 or ball_y + ball_radius > screen_height:
        ball_vel_y *= -1 * friction_factor


    # Rotate the hexagon
    hexagon_angle += rotation_speed
    if hexagon_angle >= 360:
        hexagon_angle -= 360

    # Drawing
    screen.fill(black)
    pygame.draw.polygon(screen, white, hexagon_vertices, 2) # Draw hexagon outline
    pygame.draw.circle(screen, blue, (int(ball_x), int(ball_y)), ball_radius)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()