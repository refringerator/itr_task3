#!/usr/bin/env python3

import sys

from helpers import check_params, generate_check_url
from game import Game
from menu import Menu, MenuItem
from table import show_table
from sm import InteractMachine, Engine


def main(params: list[str]):
    game = Game(moves=params)
    result = game.generate_result_function("Draw", "You win!", "Computer win!")

    menu = Menu(
        header="Available moves:",
        items=(
            [MenuItem(str(i), val, val) for i, val in enumerate(game.moves, 1)]
            + [MenuItem("0", "exit", Engine.EXIT)]
            + [MenuItem("?", "help", Engine.HELP)]
        ),
    )

    engine = Engine(
        game,
        help_action=show_table,
        finish_action=lambda: print(
            f"key = {game.secret}\n"
            f"{generate_check_url(game.secret, game.get_computer_moves())}"
        ),
        round_action=lambda user_move, game: game.set_round_result(f"{result(user_move, game.last_computer_move)} - {user_move} - {game.last_computer_move}"),      
        show_info_action=lambda game: game.prepare_round(),
    )

    def input_function():
        return menu.select("Enter your move: ")
    
    sm = InteractMachine(input_function, engine)
    sm.run()


if __name__ == "__main__":
    check_params(params := sys.argv[1:])

    try:
        main(params)
    except KeyboardInterrupt:
        print("\ncya")
