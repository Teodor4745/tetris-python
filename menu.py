import pygame
import sys
import subprocess

# Define the window sizes
WINDOW_SIZES = {
    "Small": "400x400",
    "Medium": "500x500",
    "Large": "600x600"
}

def draw_button(screen, text, position, size):
    font = pygame.font.Font(None, 36)
    text_render = font.render(text, True, (255, 255, 255))
    x, y, width, height = position
    pygame.draw.rect(screen, (0, 0, 255), position)
    screen.blit(text_render, (x + 10, y + height / 4))

def setup_screen():
    pygame.init()
    screen = pygame.display.set_mode((450, 150))
    pygame.display.set_caption("Select Window Size")

    buttons = {
        "Small": ((30, 50, 120, 50), WINDOW_SIZES["Small"]),
        "Medium": ((160, 50, 120, 50), WINDOW_SIZES["Medium"]),
        "Large": ((290, 50, 120, 50), WINDOW_SIZES["Large"])
    }

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for text, size in buttons.items():
                    pos = buttons[text][0]
                    if pos[0] <= x <= pos[0] + pos[2] and pos[1] <= y <= pos[1] + pos[3]:
                        pygame.quit()
                        # Correctly pass the window size as a string
                        subprocess.run(["python", "tetris_game.py", WINDOW_SIZES[text]])
                        return

        for text, (pos, size) in buttons.items():
            draw_button(screen, text, pos, size)

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    setup_screen()
