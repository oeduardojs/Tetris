import pygame
import random

# Inicialização do Pygame
pygame.init()

# Inicialização do mixer do Pygame para tocar música
pygame.mixer.init()

# Carregar e tocar a música
pygame.mixer.music.load("tetris.mp3")
pygame.mixer.music.set_volume(0.2)  # Ajustar o volume para 50%
pygame.mixer.music.play(-1)  # O argumento -1 faz a música tocar em loop

# Definição das cores
GRAFITE = (60, 60, 60)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CORES = [
    (255, 0, 0),    # Vermelho
    (0, 255, 0),    # Verde
    (0, 0, 255),    # Azul
    (255, 255, 0),  # Amarelo
    (255, 165, 0),  # Laranja
    (128, 0, 128),  # Roxo
    (0, 255, 255)   # Ciano
]

# Definição das formas do Tetris
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Função para rotacionar a peça
def rotate_shape(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Classe que representa uma peça
class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = 3
        self.y = 0

# Classe que representa o jogo Tetris
class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.piece = self.get_new_piece()
        self.game_over = False

    def get_new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(CORES)
        new_piece = Piece(shape, color)
        if not self.valid_position(new_piece.shape, new_piece.x, new_piece.y):
            self.game_over = True
        return new_piece

    def valid_position(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell and (
                    x + offset_x < 0 or
                    x + offset_x >= self.width or
                    y + offset_y >= self.height or
                    self.board[y + offset_y][x + offset_x]
                ):
                    return False
        return True

    def freeze_piece(self):
        for y, row in enumerate(self.piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.piece.y][x + self.piece.x] = self.piece.color
        self.clear_lines()
        self.piece = self.get_new_piece()

    def clear_lines(self):
        self.board = [row for row in self.board if any(cell == 0 for cell in row)]
        while len(self.board) < self.height:
            self.board.insert(0, [0] * self.width)

    def move_piece(self, dx, dy):
        if self.valid_position(self.piece.shape, self.piece.x + dx, self.piece.y + dy):
            self.piece.x += dx
            self.piece.y += dy
            return True
        return False

    def rotate_piece(self):
        rotated_shape = rotate_shape(self.piece.shape)
        if self.valid_position(rotated_shape, self.piece.x, self.piece.y):
            self.piece.shape = rotated_shape

# Função para desenhar um bloco com borda
def draw_block(screen, color, x, y, size=30, border_size=3):
    pygame.draw.rect(screen, PRETO, (x, y, size, size))
    pygame.draw.rect(screen, color, (x + border_size, y + border_size, size - 2 * border_size, size - 2 * border_size))

# Inicialização do jogo
screen = pygame.display.set_mode((300, 600))
clock = pygame.time.Clock()
game = Tetris(10, 20)

# Loop principal do jogo
running = True
while running:
    screen.fill(GRAFITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_piece(-1, 0)
            elif event.key == pygame.K_RIGHT:
                game.move_piece(1, 0)
            elif event.key == pygame.K_DOWN:
                game.move_piece(0, 1)
            elif event.key == pygame.K_UP:
                game.rotate_piece()
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game.move_piece(0, 1):
        game.freeze_piece()

    for y, row in enumerate(game.board):
        for x, cell in enumerate(row):
            if cell:
                draw_block(screen, cell, x * 30, y * 30)

    for y, row in enumerate(game.piece.shape):
        for x, cell in enumerate(row):
            if cell:
                draw_block(screen, game.piece.color, (game.piece.x + x) * 30, (game.piece.y + y) * 30)

    pygame.display.flip()
    clock.tick(2)  # Diminui a velocidade do jogo

    if game.game_over:
        running = False

pygame.quit()