from typing import Tuple, Optional

import numpy as np


class GameManager:
    @staticmethod
    def run(size: Tuple[int, int] = (6, 7), number: int = 4):
        board = Board(size, number)
        current_player = 1
        while not board.is_finished:
            print(board)
            print(f"Player {current_player}, input column number out of {board.available_moves()}:")
            input_value = input()
            try:
                column = int(input_value)
                if column not in board.available_moves():
                    raise ValueError
            except ValueError:
                print(f"Column number should be one of {board.available_moves()}")
                continue
            board.move(column, current_player)
            current_player = (2 - current_player) + 1

        print(board)
        print(f"Player {board.winner} won!")


class Board:
    def __init__(self, size: Tuple[int, int] = (6, 7), number: int = 4):
        if size[0] < number or size[1] < number:
            raise ValueError("Board size should be more than 4")
        self.board = np.zeros(size, dtype=int)
        self.number = number
        self.winner = None

        self.ranges = []
        self.generate_ranges()

    @property
    def columns(self) -> int:
        return self.board.size[1]

    @property
    def is_finished(self) -> bool:
        return self.winner is not None

    def __str__(self) -> str:
        result = ""
        for row in self.board:
            result += " ".join(map(Board.cell, row)) + "\n"
        return result

    @staticmethod
    def cell(value: int) -> str:
        if value == 0:
            return "."
        elif value == 1:
            return "X"
        elif value == 2:
            return "O"
        raise ValueError("Incorrect value of the cell")

    def generate_ranges(self):
        for row in range(self.board.shape[1]):
            for column in range(self.board.shape[0] - self.number + 1):
                column_range = np.arange(column, column + self.number)
                row_range = row
                self.ranges.append((column_range, row_range))
        for column in range(self.board.shape[0]):
            for row in range(self.board.shape[1] - self.number + 1):
                column_range = column
                row_range = np.arange(row, row + self.number)
                self.ranges.append((column_range, row_range))
        for row in range(self.board.shape[1] - self.number + 1):
            for column in range(self.board.shape[0] - self.number + 1):
                column_range = np.arange(column, column + self.number)
                row_range = np.arange(row, row + self.number)
                self.ranges.append((column_range, row_range))
        for row in range(self.number, self.board.shape[1]):
            for column in range(self.board.shape[0] - self.number + 1):
                column_range = np.arange(column, column + self.number)
                row_range = np.flip(np.arange(row - self.number, row))
                self.ranges.append((column_range, row_range))

    def available_moves(self):
        return np.arange(self.board.shape[1])[self.board[0] == 0]

    def move(self, column: int, current_player: int):
        if self.board[0, column] != 0:
            raise ValueError(f"Impossible move")
        non_zeros = np.nonzero(self.board[:, column])[0]
        if len(non_zeros) == 0:
            self.board[-1, column] = current_player
        else:
            self.board[non_zeros[0] - 1, column] = current_player
        self.check_winner()

    def check_winner(self):
        for column_range, row_range in self.ranges:
            winner = Board.get_winner(self.board[column_range, row_range])
            if winner is not None:
                self.winner = winner
                return

    @staticmethod
    def get_winner(line: np.ndarray) -> Optional[int]:
        for i in range(1, 3):
            if np.all(line == i):
                return i
        return None
