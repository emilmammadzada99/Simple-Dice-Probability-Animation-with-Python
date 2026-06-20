import pygame
import random

# Initial settings
pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dice Probability Simulation - Start/Stop")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TEAL = (0, 128, 128)
GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0)

# Font settings
font = pygame.font.SysFont("Arial", 16, bold=True)
btn_font = pygame.font.SysFont("Arial", 20, bold=True)

# Column (bin) settings: 11 bins for sums from 2 to 12
NUM_BINS = 11
BIN_WIDTH = 400 // NUM_BINS
BIN_START_X = 400

# Data tracking
counts = {i: 0 for i in range(2, 13)}
falling_circles = []

# Button settings
button_rect = pygame.Rect(120, 380, 160, 50)

# The simulation starts in a stopped state
is_simulating = False

# Dice drawing function
def draw_dice(surface, x, y, value):
    pygame.draw.rect(surface, BLACK, (x, y, 80, 80), 4, border_radius=15)

    dot_positions = {
        1: [(x + 40, y + 40)],
        2: [(x + 20, y + 20), (x + 60, y + 60)],
        3: [(x + 20, y + 20), (x + 40, y + 40), (x + 60, y + 60)],
        4: [(x + 20, y + 20), (x + 60, y + 20), (x + 20, y + 60), (x + 60, y + 60)],
        5: [(x + 20, y + 20), (x + 60, y + 20), (x + 40, y + 40),
            (x + 20, y + 60), (x + 60, y + 60)],
        6: [(x + 20, y + 20), (x + 60, y + 20), (x + 20, y + 40),
            (x + 60, y + 40), (x + 20, y + 60), (x + 60, y + 60)]
    }

    # Draw the dots on the dice
    for pos in dot_positions[value]:
        pygame.draw.circle(surface, BLACK, pos, 8)

# Timer event: triggered once every second
ROLL_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ROLL_EVENT, 1000)

# Initial dice values
d1, d2 = 3, 1

clock = pygame.time.Clock()
running = True

# Main game loop
while running:
    screen.fill(WHITE)

    # 1. Handle events
    for event in pygame.event.get():
        # Close the application window
        if event.type == pygame.QUIT:
            running = False

        # Check for mouse clicks on the Start/Stop button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if button_rect.collidepoint(event.pos):
                    # Toggle the simulation state
                    is_simulating = not is_simulating

        # Roll the dice only when the simulation is active
        elif event.type == ROLL_EVENT and is_simulating:
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            total = d1 + d2

            # Calculate the target column for the dice sum
            bin_index = total - 2
            target_x = BIN_START_X + (bin_index * BIN_WIDTH) + (BIN_WIDTH // 2)

            # Stack circles vertically inside the correct column
            target_y = HEIGHT - 30 - 15 - (counts[total] * 25)

            # Create a falling circle animation
            falling_circles.append({
                "x": target_x,
                "y": 0,
                "target_y": target_y,
                "val": total
            })

    # 2. Update the physics of falling circles
    for circle in falling_circles[:]:
        circle["y"] += 15

        # When the circle reaches its target, add it to the histogram count
        if circle["y"] >= circle["target_y"]:
            counts[circle["val"]] += 1
            falling_circles.remove(circle)

    # 3. Drawing operations

    # Draw a thick vertical line that divides the screen into two sections
    pygame.draw.line(screen, BLACK, (400, 0), (400, HEIGHT), 6)

    # Draw the two dice
    draw_dice(screen, 120, 220, d1)
    draw_dice(screen, 220, 120, d2)

    # Draw the Start/Stop button
    btn_color = DARK_RED if is_simulating else GREEN
    btn_text_str = "Stop" if is_simulating else "Start"

    pygame.draw.rect(screen, btn_color, button_rect, border_radius=10)
    btn_text = btn_font.render(btn_text_str, True, WHITE)
    btn_text_rect = btn_text.get_rect(center=button_rect.center)
    screen.blit(btn_text, btn_text_rect)

    # Draw histogram columns and stacked circles
    for i in range(NUM_BINS):
        val = i + 2
        x_offset = BIN_START_X + (i * BIN_WIDTH)

        # Draw vertical separators between columns
        if i > 0:
            pygame.draw.line(screen, BLACK, (x_offset, 50), (x_offset, HEIGHT - 30), 2)

        # Draw the bottom label box for each possible dice sum
        rect = pygame.Rect(x_offset, HEIGHT - 30, BIN_WIDTH, 30)
        pygame.draw.rect(screen, RED, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Draw the sum value label
        text = font.render(str(val), True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

        # Draw the circles that have already reached this column
        circle_x = x_offset + (BIN_WIDTH // 2)
        for j in range(counts[val]):
            circle_y = HEIGHT - 30 - 15 - (j * 25)
            pygame.draw.circle(screen, TEAL, (circle_x, circle_y), 10)

    # Draw circles that are still falling
    for circle in falling_circles:
        pygame.draw.circle(screen, TEAL, (circle["x"], int(circle["y"])), 10)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Close Pygame properly
pygame.quit()
