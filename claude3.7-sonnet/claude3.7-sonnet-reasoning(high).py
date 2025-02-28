import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Physics constants
GRAVITY = 0.5
FRICTION = 0.98
RESTITUTION = 0.8  # Bounciness

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
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw a small line showing the velocity vector
        pygame.draw.line(
            screen, 
            GREEN, 
            (int(self.x), int(self.y)), 
            (int(self.x + self.vx * 3), int(self.y + self.vy * 3)), 
            2
        )

class Hexagon:
    def __init__(self, center_x, center_y, radius=200):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0  # Current rotation angle in radians
        self.rotation_speed = 0.01  # Rotation speed in radians per frame
        self.vertices = self.calculate_vertices()
        
    def calculate_vertices(self):
        vertices = []
        for i in range(6):
            angle = self.angle + i * math.pi / 3
            x = self.center_x + self.radius * math.cos(angle)
            y = self.center_y + self.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices
    
    def update(self):
        self.angle += self.rotation_speed
        self.vertices = self.calculate_vertices()
    
    def draw(self, screen):
        pygame.draw.polygon(screen, BLUE, self.vertices, 2)
        # Draw center point
        pygame.draw.circle(screen, GREEN, (int(self.center_x), int(self.center_y)), 5)
    
    def check_collision(self, ball):
        # For each edge of the hexagon, check if the ball collides with it
        for i in range(6):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % 6]
            
            # Check ball collision with the line segment (p1, p2)
            if self.line_circle_collision(p1, p2, (ball.x, ball.y), ball.radius):
                self.handle_collision(ball, p1, p2)
                return True
        return False
    
    def line_circle_collision(self, p1, p2, circle_center, circle_radius):
        # Calculate the closest point on the line segment to the circle center
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])
        line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
        if line_len == 0:
            return False
            
        line_unit_vec = (line_vec[0] / line_len, line_vec[1] / line_len)
        
        # Vector from p1 to circle center
        p1_to_circle = (circle_center[0] - p1[0], circle_center[1] - p1[1])
        
        # Project p1_to_circle onto the line segment
        projection_len = max(0, min(line_len, p1_to_circle[0] * line_unit_vec[0] + p1_to_circle[1] * line_unit_vec[1]))
        
        # Calculate the closest point on the line segment
        closest_point = (
            p1[0] + projection_len * line_unit_vec[0],
            p1[1] + projection_len * line_unit_vec[1]
        )
        
        # Calculate the distance between the closest point and the circle center
        distance = math.sqrt((closest_point[0] - circle_center[0])**2 + (closest_point[1] - circle_center[1])**2)
        
        # Check if the distance is less than the circle radius
        return distance <= circle_radius
    
    def handle_collision(self, ball, p1, p2):
        # Calculate the normal vector to the wall
        wall_vec = (p2[0] - p1[0], p2[1] - p1[1])
        wall_len = math.sqrt(wall_vec[0]**2 + wall_vec[1]**2)
        if wall_len == 0:
            return
            
        wall_unit_vec = (wall_vec[0] / wall_len, wall_vec[1] / wall_len)
        
        # The normal is perpendicular to the wall (rotate the unit vector by 90 degrees)
        normal = (-wall_unit_vec[1], wall_unit_vec[0])
        
        # Calculate the tangential vector along the wall
        tangent = wall_unit_vec
        
        # Calculate the current velocity vector
        vel = (ball.vx, ball.vy)
        
        # Calculate the wall's velocity at the point of collision due to rotation
        # Find the point on the wall closest to the ball
        closest_point = self.closest_point_on_line(p1, p2, (ball.x, ball.y))
        
        # Calculate the vector from the center to this point
        r_vec = (closest_point[0] - self.center_x, closest_point[1] - self.center_y)
        r_len = math.sqrt(r_vec[0]**2 + r_vec[1]**2)
        
        if r_len > 0:
            r_unit_vec = (r_vec[0] / r_len, r_vec[1] / r_len)
            
            # Wall's tangential velocity (perpendicular to r_vec)
            wall_vel_mag = r_len * self.rotation_speed
            wall_vel = (-r_unit_vec[1] * wall_vel_mag, r_unit_vec[0] * wall_vel_mag)
        else:
            wall_vel = (0, 0)
        
        # Relative velocity of the ball with respect to the wall
        rel_vel = (vel[0] - wall_vel[0], vel[1] - wall_vel[1])
        
        # Decompose the velocity into normal and tangential components
        normal_vel = rel_vel[0] * normal[0] + rel_vel[1] * normal[1]
        tangent_vel = rel_vel[0] * tangent[0] + rel_vel[1] * tangent[1]
        
        # Only bounce if the ball is moving toward the wall
        if normal_vel < 0:
            # Reverse and dampen the normal component (bounce)
            new_normal_vel = -normal_vel * RESTITUTION
            
            # Apply friction to the tangential component
            new_tangent_vel = tangent_vel * FRICTION
            
            # Calculate the new velocity vector
            new_rel_vel = (
                new_normal_vel * normal[0] + new_tangent_vel * tangent[0],
                new_normal_vel * normal[1] + new_tangent_vel * tangent[1]
            )
            
            # Add back the wall's velocity
            ball.vx = new_rel_vel[0] + wall_vel[0]
            ball.vy = new_rel_vel[1] + wall_vel[1]
            
            # Adjust ball position to prevent sticking
            # Move the ball slightly away from the wall
            distance = self.distance_to_line(p1, p2, (ball.x, ball.y))
            penetration_depth = ball.radius - distance
            if penetration_depth > 0:
                ball.x += normal[0] * penetration_depth * 1.1
                ball.y += normal[1] * penetration_depth * 1.1
    
    def closest_point_on_line(self, p1, p2, point):
        """Find the closest point on a line segment to a given point."""
        line_vec = (p2[0] - p1[0], p2[1] - p1[1])
        line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
        if line_len == 0:
            return p1
            
        line_unit_vec = (line_vec[0] / line_len, line_vec[1] / line_len)
        p1_to_point = (point[0] - p1[0], point[1] - p1[1])
        
        # Project p1_to_point onto the line
        projection_len = max(0, min(line_len, p1_to_point[0] * line_unit_vec[0] + p1_to_point[1] * line_unit_vec[1]))
        
        return (
            p1[0] + projection_len * line_unit_vec[0],
            p1[1] + projection_len * line_unit_vec[1]
        )
    
    def distance_to_line(self, p1, p2, point):
        """Calculate the distance from a point to a line segment."""
        closest_point = self.closest_point_on_line(p1, p2, point)
        return math.sqrt((closest_point[0] - point[0])**2 + (closest_point[1] - point[1])**2)

def draw_text(screen, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Claude 3.7 - Sonnet - Reasoning (High) (28/02/2025)")
    clock = pygame.time.Clock()
    
    # Create objects
    ball = Ball(WIDTH // 2, HEIGHT // 3)
    ball.vx = 2  # Initial velocity
    ball.vy = -2
    
    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2)
    
    # Main game loop
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:  # Reset
                    ball = Ball(WIDTH // 2, HEIGHT // 3)
                    ball.vx = 2
                    ball.vy = -2
                    hexagon = Hexagon(WIDTH // 2, HEIGHT // 2)
                elif event.key == pygame.K_UP:
                    hexagon.rotation_speed += 0.005
                elif event.key == pygame.K_DOWN:
                    hexagon.rotation_speed -= 0.005
        
        if not paused:
            # Update
            ball.update()
            hexagon.update()
            hexagon.check_collision(ball)
        
        # Draw
        screen.fill(BLACK)
        hexagon.draw(screen)
        ball.draw(screen)
        
        # Display info
        draw_text(screen, f"Rotation Speed: {hexagon.rotation_speed:.3f}", 24, WIDTH // 2, 10)
        draw_text(screen, "Controls: Space = Pause, R = Reset, Up/Down = Change Speed", 20, WIDTH // 2, 40)
        draw_text(screen, f"Ball Velocity: ({ball.vx:.1f}, {ball.vy:.1f})", 20, WIDTH // 2, 70)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()