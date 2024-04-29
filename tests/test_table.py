from src.table import show_table
from src.game import Game


def test_three_moves(capsys):
    game = Game(["rock", "paper", "scissors"])
    out = """Table shows your result
+---------------+------+-------+----------+
| v PC \\ User > | rock | paper | scissors |
+---------------+------+-------+----------+
|      rock     | Draw |  Win  |   Lose   |
|     paper     | Lose |  Draw |   Win    |
|    scissors   | Win  |  Lose |   Draw   |
+---------------+------+-------+----------+
"""
    show_table(game)
    captured = capsys.readouterr()

    assert captured.out == out


def test_seven_moves(capsys):
    game = Game(["python", "rust", "ruby", "java", "php", "js", "c#"])
    out = """Table shows your result
+---------------+--------+------+------+------+------+------+------+
| v PC \\ User > | python | rust | ruby | java | php  |  js  |  c#  |
+---------------+--------+------+------+------+------+------+------+
|     python    |  Draw  | Win  | Win  | Win  | Lose | Lose | Lose |
|      rust     |  Lose  | Draw | Win  | Win  | Win  | Lose | Lose |
|      ruby     |  Lose  | Lose | Draw | Win  | Win  | Win  | Lose |
|      java     |  Lose  | Lose | Lose | Draw | Win  | Win  | Win  |
|      php      |  Win   | Lose | Lose | Lose | Draw | Win  | Win  |
|       js      |  Win   | Win  | Lose | Lose | Lose | Draw | Win  |
|       c#      |  Win   | Win  | Win  | Lose | Lose | Lose | Draw |
+---------------+--------+------+------+------+------+------+------+
"""
    show_table(game)
    captured = capsys.readouterr()

    assert captured.out == out
