from dataclasses import dataclass
import math
import random
from secret import Hmac
from enum import Enum

RoundStatus = Enum("RoudStatus", ["STARTED", "FINISHED"])


@dataclass
class Round:
    number: int
    computer_move: str
    message: str
    hmac: str
    status = RoundStatus.STARTED
    player_move: str = ""
    result: str = ""


class Game:
    result_function = lambda *args: ""

    def __init__(self, moves: list[str], secret=""):
        self.hmac = Hmac(secret_key=secret)
        self.rounds: list[Round] = []
        self.computer_moves = []
        self.moves = moves

    def get_secret(self):
        return self.hmac.secret

    def get_round_status(self):
        if not self.rounds:
            return RoundStatus.FINISHED
        return self.rounds[-1].status

    def write_result(self):
        round_result = self.result_function(
            self.get_last_user_move(), self.get_last_computer_move()
        )
        self.set_round_result(round_result)

    def generate_computer_move(self) -> str:
        if self.get_round_status() == RoundStatus.STARTED:
            return

        computer_move = random.choice(self.moves)
        round_number = self.get_round_number() + 1
        message = f"{round_number}) {computer_move}"

        round = Round(
            computer_move=computer_move,
            number=round_number,
            message=message,
            hmac=self.hmac.calc(message),
        )

        self.rounds.append(round)

    def get_last_hmac(self):
        return self.rounds[-1].hmac

    def get_round_number(self):
        return len(self.rounds)

    def prepare_round(self):
        self.generate_computer_move()
        print(f"[bold cyan]*** ROUND {self.get_round_number()} ***[/]")
        print("Computer player has made his move")
        print(f"[bold]HMAC[/] for it: [bold]{self.get_last_hmac()}\n")

    def finish_round(self):
        self.rounds[-1].status = RoundStatus.FINISHED

    def set_round_result(self, round_result):
        self.rounds[-1].result = round_result

    def set_last_user_move(self, user_move):
        self.rounds[-1].player_move = user_move

    def get_last_user_move(self):
        return self.rounds[-1].player_move

    def get_last_computer_move(self):
        return self.rounds[-1].computer_move

    def show_hello_message(self):
        print(
            "\n[bold]At the beginning of each round, the computer makes his move.\n"
            "[bold]The round number and the computer's move are concatenated and encrypted.\n"
            "[bold]Hash-based message authentication code (HMAC) of this move shown to the player.\n"
            "[bold]To ensure that the computer is not cheating, at the end, a secret key\n"
            "[bold]and a link to a website where this can be verified will be displayed.\n"
        )

    def show_round_result(self):
        last_round = self.rounds[-1]
        print(
            (
                f"Your move: [bold]{last_round.player_move}\n"
                f"Computer move: [bold]{last_round.computer_move}\n"
                f"{last_round.result}\n"
                f"{'*' * 80}"
            )
        )

    def get_computer_moves(self) -> list[str]:
        return [r.message for r in self.rounds if r.status == RoundStatus.FINISHED]

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
