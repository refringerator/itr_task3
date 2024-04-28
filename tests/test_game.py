from dataclasses import dataclass
import pytest
from src.game import Game, RoundStatus


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
    @dataclass
    class TestRound:
        message: str
        status: RoundStatus = RoundStatus.STARTED

    game = Game(["1", "2", "3", "4", "5"])
    game.rounds = [
        TestRound(message="1", status=RoundStatus.FINISHED),
        TestRound(message="2", status=RoundStatus.FINISHED),
    ]

    assert ["1", "2"] == game.get_computer_moves()


def test_get_computer_moves_unfinished_round():
    @dataclass
    class TestRound:
        message: str
        status: RoundStatus = RoundStatus.STARTED

    game = Game(["1", "2", "3", "4", "5"])
    game.rounds = [
        TestRound(message="1", status=RoundStatus.FINISHED),
        TestRound(message="2"),
    ]

    assert ["1"] == game.get_computer_moves()
