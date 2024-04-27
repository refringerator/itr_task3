import pytest
from src.game import Game


def test_draft():
    game = Game(["1", "2", "3"])
    assert 0 == game.check_winner(1, 1)


def test_winner_a():
    game = Game(["1", "2", "3", "4", "5"])
    assert game.check_winner(3, 1) > 0


def test_winner_b():
    game = Game(["1", "2", "3", "4", "5"])
    assert game.check_winner(4, 1) < 0


def test_exception():
    game = Game(["1", "2", "3", "4", "5"])
    with pytest.raises(IndexError) as excinfo:
        game.check_winner(42, 1)

    assert str(excinfo.value) == "Index out of range"


def test_get_computer_moves_finished_round():
    game = Game(["1", "2", "3", "4", "5"])
    game.computer_moves = ["1", "2", "3"]
    game.round_finished = True

    assert ["1", "2", "3"] == game.get_computer_moves()

def test_get_computer_moves_unfinished_round():
    game = Game(["1", "2", "3", "4", "5"])
    game.computer_moves = ["1", "2", "3"]
    game.round_finished = False

    assert ["1", "2"] == game.get_computer_moves()
