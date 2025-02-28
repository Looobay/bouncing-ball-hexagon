import pygame
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
FRICTION = 0.98
BALL_RADIUS = 10
HEXAGON_SIZE = 150
ROTATION_SPEED = 2  # Degrees per frame

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = BALL_RADIUS

    def apply_gravity(self):
        self.vy += GRAVITY

    def apply_friction(self):
        self.vx *= FRICTION

    def update(self):
        self.apply_gravity()
        self.apply_friction()

        self.x += self.vx
        self.y += self.vy

        # Basic boundary checks (can be removed if you want the ball to stay inside the hexagon)
        if self.x < self.radius or self.x > WIDTH - self.radius:
            self.vx *= -0.8
            self.x = max(self.radius, min(self.x, WIDTH - self.radius))
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.vy *= -0.8
            self.y = max(self.radius, min(self.y, HEIGHT - self.radius))

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def get_hexagon_points(center_x, center_y, size, angle):
    points = []
    for i in range(6):
        x = center_x + size * math.cos(math.radians(i * 60 + angle))
        y = center_y + size * math.sin(math.radians(i * 60 + angle))
        points.append((x, y))
    return points

def check_collision(ball, wall_points):
    for i in range(len(wall_points)):
        p1 = wall_points[i]
        p2 = wall_points[(i+1) % len(wall_points)]
        
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.hypot(dx, dy)
        
        if length == 0:
            continue
            
        nx = dy / length
        ny = -dx / length
        
        px = ball.x - p1[0]
        py = ball.y - p1[1]
        
        t = (px * dx + py * dy) / (length ** 2)
        t = max(0, min(1, t))
        
        closest_x = p1[0] + t * dx
        closest_y = p1[1] + t * dy
        
        dist_x = ball.x - closest_x
        dist_y = ball.y - closest_y
        distance = math.hypot(dist_x, dist_y)
        
        if distance < ball.radius:
            normal_x = (closest_x - ball.x) / distance
            normal_y = (closest_y - ball.y) / distance
            
            dot_product = ball.vx * normal_x + ball.vy * normal_y
            ball.vx -= 2 * dot_product * normal_x
            ball.vy -= 2 * dot_product * normal_y
            
            ball.vx *= 0.8  # Energy loss
            ball.vy *= 0.8
            
            penetration_x = (ball.radius - distance) * normal_x
            penetration_y = (ball.radius - distance) * normal_y
            ball.x += penetration_x
            ball.y += penetration_y

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    angle = 0
    
    ball = Ball(center_x, center_y)
    ball.vx = 5
    ball.vy = 5

    while True:
        screen.fill(WHITE)
        
        # Create rotating hexagon points
        points = get_hexagon_points(center_x, center_y, HEXAGON_SIZE, angle)
        angle += ROTATION_SPEED
        
        # Draw hexagon
        pygame.draw.lines(screen, BLUE, True, points, 2)
        
        # Update and draw ball
        ball.update()
        ball.draw(screen)
        
        # Check collisions with hexagon walls
        check_collision(ball, points)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
