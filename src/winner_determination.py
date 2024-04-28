import math


class WinnerDetermination:
    def __init__(self, moves: list[str]):
        self.moves = moves

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
                return a_winner
            elif r < 0:
                return b_winner

        return _result

    def get_scores(self, a: int | str, b: int | str) -> set[int, int]:
        r = self.check_winner(a, b)
        if r == 0:
            return (0, 0)
        elif r > 0:
            return (1, 0)
        elif r < 0:
            return (0, 1)
