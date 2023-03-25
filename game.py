import pygame
from typing_extensions import Self
import numpy as np
import random


FONT_PATH: str = "font.ttf"

WINDOW_WIDTH: int = 500
WINDOW_HEIGHT: int = 800


BOARD_WIDTH: int = 10
BOARD_HEIGHT: int = 20


BLOCK_SIZE: int = 25

# offset of board from the left hand side
BOARD_X_OFFSET: int = ((3 / 4) * WINDOW_WIDTH - BOARD_WIDTH * BLOCK_SIZE) // 2
BOARD_Y_OFFSET: int = (WINDOW_HEIGHT - BOARD_HEIGHT * BLOCK_SIZE) // 2


# offset of menu, i.e next piece, current piece, and score.
MENU_X_OFFSET: int = (WINDOW_WIDTH + BOARD_WIDTH * BLOCK_SIZE) // 2
MENU_Y_OFFSET: int = (WINDOW_HEIGHT - BOARD_HEIGHT * BLOCK_SIZE) // 2

FPS = 30


class Piece:
    # fmt: off
    PIECES: np.ndarray = np.array(
        (
            [
                [0, 0, 0, 0], 
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 2, 0, 0], 
                [0, 2, 0, 0], 
                [0, 2, 0, 0], 
                [0, 2, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 3, 3], 
                [0, 3, 3, 0],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 4, 4, 0],
                [0, 0, 4, 4],
                [0, 0, 0, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 5, 0, 0],
                [0, 5, 0, 0],
                [0, 5, 5, 0]
            
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 6, 0],
                [0, 0, 6, 0],
                [0, 6, 6, 0]
            ],
            [
                [0, 0, 0, 0],
                [0, 7, 7, 7],
                [0, 0, 7, 0],
                [0, 0, 0, 0]
            ]
        ),
        dtype=np.uint8,
    )
    # fmt: on
    COLORS: np.ndarray = np.array(
        [
            (255, 255, 255),
            (254, 251, 52),
            (1, 237, 250),
            (234, 20, 28),
            (57, 137, 47),
            (255, 145, 12),
            (221, 10, 178),
            (120, 37, 111),
        ]
    )

    def __init__(self: Self, piece_num: int = None) -> None:

        if piece_num is not None:
            assert 0 <= piece_num < len(Piece.PIECES)
            self.rep: np.ndarray = Piece.PIECES[piece_num]
        else:
            self.rep: np.ndarray = random.choice(Piece.PIECES)

    @property
    def array(self: Self) -> np.ndarray:
        return self.rep

    def __repr__(self: Self) -> str:
        return "\n".join("".join(row) for row in self.rep)

    __str__ = __repr__


class Tetris:
    def __init__(self: Self) -> None:
        pygame.font.init()

        self.window: pygame.Surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.font: pygame.font.Font = pygame.font.Font(FONT_PATH, 24)

        self.current_piece_msg: pygame.Surface = self.font.render(
            "Current Piece", False, (0, 0, 0)
        )
        self.next_piece_msg: pygame.Surface = self.font.render(
            "Next Piece", False, (0, 0, 0)
        )

        self.current_piece: Piece = Piece()
        self.next_piece: Piece = Piece()

        self.board: np.ndarray = np.random.randint(
            6, size=(BOARD_HEIGHT, BOARD_WIDTH), dtype=np.uint8
        )

        self.running: bool = True
        self.game_over: bool = False

    def numpy_to_surface(self: Self, x: np.ndarray, show_grid: bool = True) -> None:

        y: np.ndarray = Piece.COLORS[x].repeat(BLOCK_SIZE, 0).repeat(BLOCK_SIZE, 1)

        BLACK: np.ndarray = np.array([0, 0, 0])


        if not show_grid:
            pass

        y[np.arange(0, y.shape[0], BLOCK_SIZE), :] = BLACK
        y[:, np.arange(0, y.shape[1], BLOCK_SIZE)] = BLACK

        y[y.shape[0] - 1, :] = BLACK
        y[:, y.shape[1] - 1] = BLACK

        return pygame.surfarray.make_surface(y.swapaxes(0, 1))

    def display(self: Self) -> None:
        self.window.fill((255, 255, 255))

        self.window.blit(
            self.numpy_to_surface(self.board), (BOARD_X_OFFSET, BOARD_Y_OFFSET)
        )

        self.window.blit(
            self.current_piece_msg, (MENU_X_OFFSET - 40, MENU_Y_OFFSET - 50)
        )
        self.window.blit(self.next_piece_msg, (MENU_X_OFFSET - 25, MENU_Y_OFFSET + 150))

        self.window.blit(
            self.numpy_to_surface(self.current_piece.array),
            (MENU_X_OFFSET, MENU_Y_OFFSET),
        )

        self.window.blit(
            self.numpy_to_surface(self.next_piece.array),
            (MENU_X_OFFSET, MENU_Y_OFFSET + 200),
        )

        pygame.display.flip()

    def step(self: Self, choice: int = None) -> None:

        self.poll_events()

        if choice is None:
            # choice = input("Select a row: ")
            pass

        self.display()

    def poll_events(self: Self) -> None:

        for event in pygame.event.get():

            match event.type:

                case pygame.QUIT:
                    self.running = False

                case pygame.MOUSEBUTTONDOWN:
                    print("hi")
                    self.next_piece = Piece()

    def reset_game(self: Self) -> None:
        pass

    def run(self: Self) -> None:
        clock: pygame.time.Clock = pygame.time.Clock()

        while self.running:

            if self.game_over:
                self.reset_game()
                self.game_over = False

            self.step()

            clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    game: Tetris = Tetris()
    game.run()
