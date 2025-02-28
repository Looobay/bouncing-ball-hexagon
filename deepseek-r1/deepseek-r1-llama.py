import pygame
import math

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAVITY = 0.5
FRICTION = 0.98
BOUNCE_DAMPING = 0.8

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = 0
        self.vy = 0
        self.radius = 10

    def apply_gravity(self):
        self.vy += GRAVITY

    def apply_friction(self):
        self.vx *= FRICTION
        self.vy *= FRICTION

    def update(self):
        self.apply_gravity()
        self.apply_friction()
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    ball = Ball()
    rotation_angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear screen
        screen.fill(WHITE)

        # Draw spinning hexagon
        center = (WIDTH // 2, HEIGHT // 2)
        radius = 200
        rotation_angle += 1

        # Calculate hexagon vertices
        vertices = []
        for i in range(6):
            angle = math.radians(60 * i + rotation_angle)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            vertices.append((x, y))

        # Draw hexagon
        for i in range(6):
            start = vertices[i]
            end = vertices[(i + 1) % 6]
            pygame.draw.line(screen, (0, 0, 0), start, end, 2)

        # Update ball position
        ball.update()

        # Check collisions with hexagon walls
        for i in range(6):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % 6]

            # Line equation: ax + by + c = 0
            a = y2 - y1
            b = x1 - x2
            c = x2*y1 - x1*y2

            # Calculate distance from ball to line
            distance = (a * ball.x + b * ball.y + c) / math.sqrt(a**2 + b**2)
            if distance < ball.radius:
                # Calculate reflection
                normal_x = a / math.sqrt(a**2 + b**2)
                normal_y = b / math.sqrt(a**2 + b**2)
                
                dot_product = ball.vx * normal_x + ball.vy * normal_y
                ball.vx = (ball.vx - 2 * dot_product * normal_x) * BOUNCE_DAMPING
                ball.vy = (ball.vy - 2 * dot_product * normal_y) * BOUNCE_DAMPING

        # Draw ball
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
