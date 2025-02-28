import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Ball properties
ball_radius = 10
ball_pos = [width // 2, height // 2]
ball_vel = [0, 0]
gravity = 0.5
friction = 0.99

# Hexagon properties
hexagon_radius = 200
hexagon_center = [width // 2, height // 2]
hexagon_rotation = 0
hexagon_rotation_speed = 0.01

def draw_hexagon(center, radius, rotation):
    points = []
    for i in range(6):
        angle = math.radians(i * 60 + rotation)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(screen, white, points, 1)

def update_ball():
    global ball_pos, ball_vel
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_vel[1] += gravity
    ball_vel[0] *= friction
    ball_vel[1] *= friction

    # Collision with hexagon
    for i in range(6):
        angle = math.radians(i * 60 + hexagon_rotation)
        normal = [math.cos(angle), math.sin(angle)]
        edge_point = [hexagon_center[0] + hexagon_radius * normal[0], hexagon_center[1] + hexagon_radius * normal[1]]
        edge_vector = [edge_point[0] - hexagon_center[0], edge_point[1] - hexagon_center[1]]
        ball_to_edge = [ball_pos[0] - edge_point[0], ball_pos[1] - edge_point[1]]
        dot_product = ball_to_edge[0] * normal[0] + ball_to_edge[1] * normal[1]
        if dot_product < ball_radius:
            ball_vel[0] -= 2 * dot_product * normal[0]
            ball_vel[1] -= 2 * dot_product * normal[1]

    # Collision with screen edges
    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > width:
        ball_vel[0] = -ball_vel[0]
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > height:
        ball_vel[1] = -ball_vel[1]

def main():
    global hexagon_rotation
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)
        draw_hexagon(hexagon_center, hexagon_radius, hexagon_rotation)
        pygame.draw.circle(screen, red, [int(ball_pos[0]), int(ball_pos[1])], ball_radius)
        update_ball()
        hexagon_rotation += hexagon_rotation_speed

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
