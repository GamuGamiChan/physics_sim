import math
import pygame
import pymunk.pygame_util

PIXELS_PER_METER = 100.0


def to_screen(p):
  return int(p[0] * PIXELS_PER_METER), int(p[1] * PIXELS_PER_METER)


pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation Sloped Box (30 Degrees)")
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 1000)  # Adjusted gravity for pixel-scale physics

# Box properties
mass = 5.0
box_size_m = 0.4
box_w_px = box_size_m * PIXELS_PER_METER
box_h_px = box_size_m * PIXELS_PER_METER

moment = pymunk.moment_for_box(mass, (box_w_px, box_h_px))
body = pymunk.Body(mass, moment)

# Box start position (placed on the slope)
body.position = (1.5 * PIXELS_PER_METER, 2.3 * PIXELS_PER_METER)

shape = pymunk.Poly.create_box(body, (box_w_px, box_h_px))
shape.friction = 0.4
space.add(body, shape)

# 30-Degree Sloped Floor
floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_start = (0.5 * PIXELS_PER_METER, 2.0 * PIXELS_PER_METER)

angle_deg = 30
angle_rad = math.radians(angle_deg)
floor_length_px = 4.0 * PIXELS_PER_METER

floor_end = (
    floor_start[0] + floor_length_px * math.cos(angle_rad),
    floor_start[1] + floor_length_px * math.sin(angle_rad),
)

floor_shape = pymunk.Segment(floor_body, floor_start, floor_end, 5)
floor_shape.friction = 0.2
space.add(floor_body, floor_shape)

dt = 1.0 / 60.0
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
step_count = 0

print(
    "Simulation started. Position and velocity will be printed every 15 steps."
)

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  space.step(dt)

  # Convert position and velocity for display
  velocity_m_s = body.velocity.x / PIXELS_PER_METER
  position_m_x = body.position.x / PIXELS_PER_METER

  step_count += 1
  if step_count % 15 == 0:
    print(
        f"Position X: {position_m_x:5.2f} m | Speed X:"
        f" {velocity_m_s:5.3f} m/s"
    )

  # Draw background and objects
  screen.fill((255, 255, 255))
  space.debug_draw(draw_options)

  pygame.display.flip()
  clock.tick(60)

pygame.quit()