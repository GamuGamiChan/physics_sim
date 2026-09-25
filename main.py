import pygame
import pymunk.pygame_util

PIXELS_PER_METER = 100.0

def to_screen(p):
  return int(p[0] * PIXELS_PER_METER), int(p[1] * PIXELS_PER_METER)


pygame.init()
width, height = 400, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation Flat Box with Impulse")
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 10)

# 2. Defines
mass = 2.0
box_size_m = 0.4
box_w_px = box_size_m * PIXELS_PER_METER
box_h_px = box_size_m * PIXELS_PER_METER

moment = pymunk.moment_for_box(mass, (box_w_px, box_h_px))
body = pymunk.Body(mass, moment)

# Box start pos
body.position = (1.0 * PIXELS_PER_METER, 2.0 * PIXELS_PER_METER)

shape = pymunk.Poly.create_box(body, (box_w_px, box_h_px))
shape.friction = 0.2  # Friction coefficient
space.add(body, shape)

# Floor
floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
floor_start = (0.5 * PIXELS_PER_METER, 2.2 * PIXELS_PER_METER)
floor_end = (3.5 * PIXELS_PER_METER, 2.2 * PIXELS_PER_METER)
floor_shape = pymunk.Segment(floor_body, floor_start, floor_end, 5)
floor_shape.friction = 0.2
space.add(floor_body, floor_shape)

# NS at 10 * 1
push_impulse = (10, 0)
body.apply_impulse_at_local_point(push_impulse, (0, 0))

dt = 1.0 / 60.0
draw_options = pymunk.pygame_util.DrawOptions(screen)

running = True
step_count = 0

print("Simulation started. Position and velocity will be printed every 15 steps.")

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  space.step(dt)

  # Convert position and velocity from pixels to meters for display
  velocity_m_s = body.velocity.x / PIXELS_PER_METER
  position_m_x = (body.position.x / PIXELS_PER_METER) - 1

  step_count += 1
  if step_count % 15 == 0:
    print(
        f"Position: {position_m_x:5.2f} M | Speed:"
        f" {velocity_m_s:5.3f} M/S"
    )

  # draw background and objects
  screen.fill((255, 255, 255))
  space.debug_draw(draw_options)

  pygame.display.flip()
  clock.tick(60)

pygame.quit()