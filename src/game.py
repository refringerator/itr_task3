from dataclasses import dataclass
from collections import namedtuple
import random
from functools import reduce
from table import show_rich_table
from winner_determination import WinnerDetermination as WD
from secret import Hmac
from enum import Enum

RoundStatus = Enum("RoudStatus", ["STARTED", "FINISHED"])
Scores = namedtuple("Scores", ["Player", "Computer"])


@dataclass
class Round:
    number: int
    computer_move: str
    message: str
    hmac: str
    status = RoundStatus.STARTED
    player_move: str = ""
    result: str = ""
    scores: Scores = (0, 0)


class Game:
    def _result_function(*args):
        return ""

    result_function = _result_function

    def __init__(self, moves: list[str], secret=""):
        self.hmac = Hmac(secret_key=secret)
        self.rounds: list[Round] = []
        self.computer_moves = []
        self.moves = moves
        self.wd = WD(moves)

    def set_result_function(self, *args):
        self.result_function = self.wd.generate_result_function(*args)

    def get_secret(self):
        return self.hmac.secret

    def get_game_scores(self) -> Scores:
        add_tuples = lambda a, b: (a[0] + b[0], a[1] + b[1])
        rounds_score = [r.scores for r in self.rounds]
        total_scores = reduce(add_tuples, rounds_score, (0, 0))
        return Scores(*total_scores)

    def get_round_status(self):
        if not self.rounds:
            return RoundStatus.FINISHED
        return self.rounds[-1].status

    def set_round_scores(self, scores: Scores):
        self.rounds[-1].scores = scores

    def write_result(self):
        user_move = self.get_last_user_move()
        computer_move = self.get_last_computer_move()
        round_result = self.result_function(user_move, computer_move)
        self.set_round_result(round_result)
        self.set_round_scores(self.wd.get_scores(user_move, computer_move))

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
        scores = self.get_game_scores()
        print(f"[bold cyan]*** ROUND {self.get_round_number()} ***[/]")
        print(
            f"[bold cyan]*** GAME SCORES: Player {scores.Player}:{scores.Computer} Computer ***[/]"
        )
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

    def show_finish_message(self):
        finished_rounds = [r for r in self.rounds if r.status == RoundStatus.FINISHED]
        if not finished_rounds:
            return

        show_rich_table(
            title="Messages to check",
            columns=["Message", "HMAC"],
            caption="All messages and their encrypted form for the entire game are collected here",
            rows=[(r.message, r.hmac) for r in finished_rounds],
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
