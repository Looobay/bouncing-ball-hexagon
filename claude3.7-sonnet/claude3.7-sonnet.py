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
FRICTION = 0.99
ELASTICITY = 0.8

class Ball:
    def __init__(self, x, y, radius=15):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.color = RED
    
    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Update position
        self.x += self.vx
        self.y += self.vy
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class Hexagon:
    def __init__(self, center_x, center_y, radius=200):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0
        self.rotation_speed = 0.01
        self.color = BLUE
        self.num_sides = 6
        self.vertices = self.calculate_vertices()
        self.lines = self.calculate_lines()
    
    def calculate_vertices(self):
        vertices = []
        for i in range(self.num_sides):
            angle = self.angle + 2 * math.pi * i / self.num_sides
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices
    
    def calculate_lines(self):
        lines = []
        for i in range(self.num_sides):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % self.num_sides]
            lines.append((p1, p2))
        return lines
    
    def update(self):
        self.angle += self.rotation_speed
        self.vertices = self.calculate_vertices()
        self.lines = self.calculate_lines()
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.vertices, 2)


def distance_point_to_line(point, line):
    """Calculate the distance from a point to a line segment and the closest point on the line."""
    x, y = point
    (x1, y1), (x2, y2) = line
    
    # Calculate the squared length of the line segment
    l2 = (x2 - x1)**2 + (y2 - y1)**2
    
    # If the line segment has zero length, return the distance to one of the endpoints
    if l2 == 0:
        return math.sqrt((x - x1)**2 + (y - y1)**2), (x1, y1)
    
    # Calculate the projection ratio t
    t = max(0, min(1, ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / l2))
    
    # Calculate the closest point on the line segment
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    # Calculate the distance to the closest point
    distance = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)
    
    return distance, (closest_x, closest_y)


def handle_collision(ball, hexagon):
    for line in hexagon.lines:
        distance, closest_point = distance_point_to_line((ball.x, ball.y), line)
        
        # Check for collision
        if distance <= ball.radius:
            # Calculate normal vector of the line
            (x1, y1), (x2, y2) = line
            line_vec = np.array([x2 - x1, y2 - y1])
            line_length = np.linalg.norm(line_vec)
            if line_length > 0:
                line_vec = line_vec / line_length
            
            # Calculate normal vector (perpendicular to the line)
            normal = np.array([-line_vec[1], line_vec[0]])
            
            # Calculate ball's velocity vector
            velocity = np.array([ball.vx, ball.vy])
            
            # Calculate the velocity of the rotating line at the point of contact
            # Angular velocity (rad/frame) * radius (distance from center)
            point_distance = math.sqrt((closest_point[0] - hexagon.center_x)**2 + 
                                      (closest_point[1] - hexagon.center_y)**2)
            
            # Calculate tangential velocity at the point of collision
            tangent = np.array([line_vec[0], line_vec[1]])
            wall_velocity = hexagon.rotation_speed * point_distance
            wall_velocity_vec = tangent * wall_velocity
            
            # Adjust ball's velocity for the moving wall
            velocity = velocity - wall_velocity_vec
            
            # Calculate reflection
            reflection = velocity - 2 * np.dot(velocity, normal) * normal
            
            # Apply elasticity to the reflected velocity
            reflection = reflection * ELASTICITY
            
            # Add back the wall's velocity
            reflection = reflection + wall_velocity_vec
            
            # Update ball's velocity
            ball.vx, ball.vy = reflection
            
            # Move the ball outside the line to prevent getting stuck
            overlap = ball.radius - distance
            ball.x += normal[0] * overlap * 1.1
            ball.y += normal[1] * overlap * 1.1
            
            return True
    
    return False


def main():
    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Claude 3.7 - Sonnet (28/02/2025)")
    clock = pygame.time.Clock()
    
    # Create the ball and hexagon
    ball = Ball(WIDTH/2, HEIGHT/2)
    hexagon = Hexagon(WIDTH/2, HEIGHT/2)
    
    # Give the ball an initial velocity
    ball.vx = 5
    ball.vy = -8
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    hexagon.rotation_speed = -hexagon.rotation_speed
                elif event.key == pygame.K_UP:
                    hexagon.rotation_speed *= 1.5
                elif event.key == pygame.K_DOWN:
                    hexagon.rotation_speed /= 1.5
        
        # Update the ball and hexagon
        ball.update()
        hexagon.update()
        
        # Handle collisions
        handle_collision(ball, hexagon)
        
        # Clear the screen
        screen.fill(BLACK)
        
        # Draw the ball and hexagon
        hexagon.draw(screen)
        ball.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()