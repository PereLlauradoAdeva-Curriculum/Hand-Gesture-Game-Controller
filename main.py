import pygame
import random
import time

pygame.init()

# Color definitions (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

# Window and game setup
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Function to display centered messages on screen
def message(msg, color, y_offset=0):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(width/2, height/2 + y_offset))
    win.blit(text, text_rect)

# Main game loop
def game_loop(get_external_direction):
    snake_pos = [100, 50]             # Initial head position
    snake_body = [[100, 50]]          # Initial body (1 segment)
    snake_dir = 'RIGHT'               # Initial direction
    change_to = snake_dir             # Next direction to apply

    score = 0
    speed = 7                         # Game speed (FPS)

    # Random initial food position (aligned to grid)
    food_pos = [random.randrange(1, (width//10)) * 10,
                random.randrange(1, (height//10)) * 10]
    food_spawn = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Get hand gesture direction (external input)
        new_dir = get_external_direction()
        # Update direction if it's not the opposite of current
        if new_dir == "UP" and snake_dir != "DOWN":
            change_to = "UP"
        elif new_dir == "DOWN" and snake_dir != "UP":
            change_to = "DOWN"
        elif new_dir == "LEFT" and snake_dir != "RIGHT":
            change_to = "LEFT"
        elif new_dir == "RIGHT" and snake_dir != "LEFT":
            change_to = "RIGHT"

        snake_dir = change_to

        # Move the snake head in the selected direction
        if snake_dir == 'UP':
            snake_pos[1] -= 10
        elif snake_dir == 'DOWN':
            snake_pos[1] += 10
        elif snake_dir == 'LEFT':
            snake_pos[0] -= 10
        elif snake_dir == 'RIGHT':
            snake_pos[0] += 10

        # Insert new head position
        snake_body.insert(0, list(snake_pos))
        # Check if food is eaten
        if snake_pos == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()  # Remove tail segment

        # Generate new food if needed
        if not food_spawn:
            food_pos = [random.randrange(1, (width//10)) * 10,
                        random.randrange(1, (height//10)) * 10]
        food_spawn = True

        # Clear screen
        win.fill(BLACK)

        # Draw snake body
        for block in snake_body:
            pygame.draw.rect(win, GREEN, pygame.Rect(block[0], block[1], 10, 10))

        # Draw food
        pygame.draw.rect(win, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Draw score
        score_text = font.render("Score: " + str(score), True, WHITE)
        win.blit(score_text, [10, 10])

        # Game over conditions: hit wall or self
        if (snake_pos[0] < 0 or snake_pos[0] >= width or
            snake_pos[1] < 0 or snake_pos[1] >= height or
            snake_pos in snake_body[1:]):
            message("GAME OVER", RED)
            pygame.display.flip()
            time.sleep(2)
            start_screen(get_external_direction)  # Return to menu
            return

        pygame.display.update()
        clock.tick(speed)

# Start screen with a play button
def start_screen(get_external_direction):
    button = pygame.Rect(width/2 - 60, height/2 + 30, 120, 40)
    while True:
        win.fill(BLACK)
        message("Press the button to start", WHITE, y_offset=-30)
        pygame.draw.rect(win, GREEN, button)
        text = font.render("PLAY", True, BLACK)
        win.blit(text, (button.x + 20, button.y + 8))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    game_loop(get_external_direction)
                    return

# Entry point: run the game with MediaPipe hand tracker
if __name__ == "__main__":
    from handDetectorMP import HandTracker
    tracker = HandTracker()
    try:
        start_screen(tracker.get_direction)
    finally:
        tracker.release()
        pygame.quit()
