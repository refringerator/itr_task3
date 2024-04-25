from dataclasses import dataclass
import math
import random


@dataclass
class Round:
    number: int
    computer_move: str
    hmac: str
    player_move: str
    finished: bool


class Game:
    def __init__(self, moves: list[str]) -> None:
        self.moves = moves
        self.rounds = []
        self.n = 0
        self.computer_moves = []

    def generate_computer_move(self) -> str:
        self.n += 1
        move = random.choice(self.moves)
        message = f"{self.n}) {move}"
        self.computer_moves.append(message)

        return message, move

    def check_winner(self, a: int | str, b: int | str) -> int:
        n = len(self.moves)
        if isinstance(a, str):
            a = self.moves.index(a)
        if isinstance(b, str):
            b = self.moves.index(b)

        if a >= n or b >= n or a < 0 or b < 0:
            raise IndexError("Index out of range")

        p = math.floor(n / 2)
        return (a - b + p + n) % n - p

    def generate_result_function(self, draw: str, a_winner: str, b_winner: str):
        def _result(a: int | str, b: int | str) -> str:
            r = self.check_winner(a, b)
            if r == 0:
                return draw
            elif r > 0:
                return b_winner
            elif r < 0:
                return a_winner

        return _result
