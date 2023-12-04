import random
import sys

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COLORS = [RED, BLUE, GREEN]

SHAPES = [
    [
        ['.....',
         '.....',
         '.....',
         '.OOOO',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..']
    ],
    [
        ['.....',
         '.....',
         '..OO.',
         '..OO.',
         '.....'],
    ],
    [
        ['.....',
         '.....',
         '..O..',
         '.OOO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....']
    ],
    [
        ['.....',
         '.....',
         '..OO.',
         '.OO..',
         '.....'],
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '..O..',
         '..O.',
         '..OO.',
         '.....'],
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....']
    ],

]


class Shape:
    def __init__(self, x, y, shape):
        self.color = random.choice(COLORS)
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = 0


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        return Shape(self.width // 2, 0, shape)

    def valid_move(self, piece, x, y, rotation):
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    if not (0 <= piece.x + j + x < self.width) or \
                            not (0 <= piece.y + i + y < self.height) or \
                            (self.grid[piece.y + i + y][piece.x + j + x] != 0):
                        return False
        return True

    def clear_lines(self):
        lines_cleared = 0
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def lock_piece(self, piece):
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color

        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100

        self.current_piece = self.new_piece()

        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared

    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

        if self.current_piece:
            for i, row in enumerate(
                    self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, self.current_piece.color, (
                            (self.current_piece.x + j) * SQUARE_SIZE, (self.current_piece.y + i) * SQUARE_SIZE,
                            SQUARE_SIZE - 1,
                            SQUARE_SIZE - 1))


def draw_scores(screen, score, high_score, x, y):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (x, y))
    screen.blit(high_score_text, (x, y + 40))

def draw_game_over(screen, x, y):
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (x, y))

def read_high_score(file_path):
    try:
        with open(file_path, 'r') as file:
            high_score = file.read()
            return int(high_score) if high_score else 0
    except FileNotFoundError:
        return 0

def save_high_score(file_path, score):
    with open(file_path, 'w') as file:
        file.write(str(score))


def run_game(width,height):
    pygame.init()
    pygame.font.init()
    if width and height:
        WIDTH = width
        HEIGHT = height
    else:
        WIDTH, HEIGHT = 400, 400

    global GRID_WIDTH, SQUARE_SIZE

    if WIDTH <= 400:
        GRID_WIDTH = 12
    elif WIDTH <= 500:
        GRID_WIDTH = 16
    else:
        GRID_WIDTH = 20

    SQUARE_SIZE = WIDTH // GRID_WIDTH
    GRID_HEIGHT = HEIGHT // SQUARE_SIZE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()

    game = Tetris(GRID_WIDTH, GRID_HEIGHT)

    fall_time = 0
    fall_speed = 80

    high_score_file = 'high_score.txt'
    high_score = read_high_score(high_score_file)

    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1
                if event.key == pygame.K_RIGHT:
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1
                if event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                if event.key == pygame.K_UP:
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1
                if event.key == pygame.K_SPACE:
                    while game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                    game.lock_piece(game.current_piece)

        delta_time = clock.get_rawtime()

        fall_time += delta_time
        if fall_time >= fall_speed:

            game.update()

            fall_time = 0

        draw_scores(screen, game.score, high_score, 10, 10)

        game.draw(screen)
        if game.game_over:

            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    game = Tetris(WIDTH // SQUARE_SIZE, HEIGHT // SQUARE_SIZE)
                    game.game_over = False
                    continue

            if game.score > high_score:
                high_score = game.score
                save_high_score(high_score_file, high_score)
            if event.type == pygame.KEYDOWN:

                game = Tetris(WIDTH // SQUARE_SIZE, HEIGHT // SQUARE_SIZE)

        pygame.display.flip()
        clock.tick(60)
