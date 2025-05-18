import pygame
import math

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = 5
        self.vy = -10
        self.radius = 10
        self.friction = 0.98
        self.gravity = 0.1

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= self.friction
        self.vy *= self.friction

class Hexagon:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.size = 200
        self.angle = 0
        self.speed = 2

    def update(self):
        self.angle += self.speed

    def get_points(self):
        points = []
        for i in range(6):
            angle = self.angle + i * math.pi / 3
            px = self.x + math.cos(angle) * self.size
            py = self.y + math.sin(angle) * self.size
            points.append((px, py))
        return points

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    hexagon = Hexagon()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball.update()
        hexagon.update()

        # Collision with hexagon walls
        points = hexagon.get_points()
        for i in range(6):
            p1 = points[i]
            p2 = points[(i + 1) % 6]
            if is_collision(ball.x, ball.y, ball.radius, p1, p2):
                ball.vx = -ball.vx * 0.8
                ball.vy = -ball.vy * 0.8

        # Collision with window edges
        if ball.x - ball.radius < 0 or ball.x + ball.radius > WIDTH:
            ball.vx = -ball.vx
        if ball.y - ball.radius < 0 or ball.y + ball.radius > HEIGHT:
            ball.vy = -ball.vy * 0.8

        screen.fill(WHITE)
        pygame.draw.polygon(screen, (0, 0, 0), points, 2)
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), ball.radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def is_collision(x, y, radius, p1, p2):
    # Calculate distance from point to line segment
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    t = ((x - p1[0]) * dx + (y - p1[1]) * dy) / (dx ** 2 + dy ** 2)
    t = max(0, min(1, t))
    distance = math.sqrt((x - (p1[0] + t * dx)) ** 2 + (y - (p1[1] + t * dy)) ** 2)
    return distance < radius

if __name__ == "__main__":
    main()
