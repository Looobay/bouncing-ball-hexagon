import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gemini 2.0 Flash (28/02/2025)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 0
gravity = 0.5
friction = 0.01

# Hexagon properties
hexagon_radius = 200
hexagon_x = WIDTH // 2
hexagon_y = HEIGHT // 2
rotation_speed = 0.01
angle = 0

# Function to calculate hexagon vertices
def calculate_hexagon_vertices(x, y, radius, angle):
  vertices = []
  for i in range(6):
    angle_rad = math.radians(60 * i) + angle
    vertex_x = x + radius * math.cos(angle_rad)
    vertex_y = y + radius * math.sin(angle_rad)
    vertices.append((vertex_x, vertex_y))
  return vertices

# Function to check collision with a line segment
def check_collision(ball_x, ball_y, ball_radius, p1, p2):
  # Calculate distance from ball center to the line
  x1, y1 = p1
  x2, y2 = p2
  dx = x2 - x1
  dy = y2 - y1

  # Calculate the parameter t
  t = ((ball_x - x1) * dx + (ball_y - y1) * dy) / (dx * dx + dy * dy)

  # Clamp t to the range [0, 1]
  t = max(0, min(1, t))

  # Find the closest point on the line segment
  closest_x = x1 + t * dx
  closest_y = y1 + t * dy

  # Calculate the distance from the ball center to the closest point
  distance = math.sqrt((ball_x - closest_x) ** 2 + (ball_y - closest_y) ** 2)

  # If the distance is less than the ball radius, there is a collision
  if distance <= ball_radius:
    # Calculate the normal vector
    normal_x = -(y2 - y1)
    normal_y = dx

    # Normalize the normal vector
    normal_length = math.sqrt(normal_x**2 + normal_y**2)
    normal_x /= normal_length
    normal_y /= normal_length

    # Calculate the dot product of the ball's velocity and the normal vector
    dot_product = ball_speed_x * normal_x + ball_speed_y * normal_y

    # Reflect the ball's velocity
    ball_speed_x -= 2 * dot_product * normal_x
    ball_speed_y -= 2 * dot_product * normal_y

    # Add a small offset to prevent sticking
    ball_x += normal_x * (ball_radius - distance)
    ball_y += normal_y * (ball_radius - distance)

    return True
  return False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
  # Event handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Update ball position
  ball_x += ball_speed_x
  ball_y += ball_speed_y

  # Apply gravity
  ball_speed_y += gravity

  # Apply friction
  ball_speed_x *= 1 - friction
  ball_speed_y *= 1 - friction

  # Calculate hexagon vertices
  vertices = calculate_hexagon_vertices(
      hexagon_x, hexagon_y, hexagon_radius, angle
  )

  # Collision detection with hexagon walls
  for i in range(6):
    p1 = vertices[i]
    p2 = vertices[(i + 1) % 6]
    check_collision(ball_x, ball_y, ball_radius, p1, p2)

  # Keep the ball within the screen bounds (simple walls)
  if ball_x - ball_radius < 0:
    ball_x = ball_radius
    ball_speed_x *= -1
  if ball_x + ball_radius > WIDTH:
    ball_x = WIDTH - ball_radius
    ball_speed_x *= -1
  if ball_y - ball_radius < 0:
    ball_y = ball_radius
    ball_speed_y *= -1
  if ball_y + ball_radius > HEIGHT:
    ball_y = HEIGHT - ball_radius
    ball_speed_y *= -1

  # Update hexagon rotation
  angle += rotation_speed

  # Drawing
  screen.fill(BLACK)

  # Draw hexagon
  pygame.draw.polygon(screen, WHITE, vertices, 2)

  # Draw ball
  pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)

  # Update display
  pygame.display.flip()

  # Control frame rate
  clock.tick(60)

# Quit Pygame
pygame.quit()