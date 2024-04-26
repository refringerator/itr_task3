#!/usr/bin/env python3

import sys
from secret import Hmac

from helpers import check_params, generate_check_url
from game import Game
from menu import Menu, MenuItem
from table import show_table
from sm import InteractMachine, Lol


def main(params: list[str]):
    hmac = Hmac()
    game = Game(moves=params)
    result = game.generate_result_function("Draw", "You win!", "Computer win!")

    menu_action = None
    menu_items = (
        [MenuItem(str(i), val, menu_action) for i, val in enumerate(game.moves, 1)]
        + [MenuItem("0", "exit", Lol.EXIT)]
        + [MenuItem("?", "help", Lol.HELP)]
    )

    menu = Menu(menu_items, header="Available moves:")

    lol = Lol(help_action=lambda: show_table(game))
    sm = InteractMachine(lol)
    sm.run()

    def pre_ask():
        message, c_move = game.generate_computer_move()
        hmac_code = hmac.calc(message)

        text = f"HMAC: {hmac_code}"
        print(text)
        return c_move

    while not sm.current_state.final:
        c_move = pre_ask()

        sm.send("input", menu.select("Enter your move: "))

        if lol.ans == Lol.EXIT:
            print(f"key = {hmac.secret}")
            print(generate_check_url(hmac.secret, game.computer_moves))

        elif lol.ans == Lol.HELP:
            pass

        else:
            umi = int(lol.ans) - 1

            text = (
                f"Your move: {params[umi]}\n"
                f"Computer move: {c_move}\n"
                f"{result(umi, c_move)}\n"
                f"{'*' * 80}"
            )

            print(text)


if __name__ == "__main__":
    check_params(params:=sys.argv[1:])

    try:
        main(params)
    except KeyboardInterrupt:
        print("\ncya")
