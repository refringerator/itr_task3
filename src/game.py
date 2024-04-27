from dataclasses import dataclass
import math
import random
from secret import Hmac


@dataclass
class Round:
    number: int
    computer_move: str
    hmac: str
    player_move: str
    finished: bool


class Game:
    def __init__(self, moves: list[str], secret=""):
        self.hmac = Hmac(secret_key=secret)
        self.secret = self.hmac.secret
        self.moves = moves
        self.rounds = []
        self.round_number = 0
        self.computer_moves = []
        self.last_computer_move = ""
        self.last_user_move = ""
        self.round_result = ""
        self.round_finished = True

    def generate_computer_move(self) -> str:
        if self.round_finished:
            self.round_finished = False
            self.round_number += 1
            self.last_computer_move = random.choice(self.moves)
            message = f"{self.round_number}) {self.last_computer_move}"
            self.computer_moves.append(message)
        
        return self.computer_moves[-1]

    def prepare_round(self):
        message = self.generate_computer_move()
        hmac_code = self.hmac.calc(message)
        print(f"HMAC: {hmac_code}")

    def finish_round(self):
        self.round_finished = True

    def set_round_result(self, round_result):
        self.round_result = round_result

    def set_last_user_move(self, user_move):
        self.last_user_move = user_move

    def show_round_result(self):
        print(
            (
                f"Your move: {self.last_user_move}\n"
                f"Computer move: {self.last_computer_move}\n"
                f"{self.round_result}\n"
                f"{'*' * 80}"
            )
        )

    def get_computer_moves(self) -> list[str]:
        last_move = None if self.round_finished else -1
        return self.computer_moves[:last_move]

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
