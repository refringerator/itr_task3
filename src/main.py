#!/usr/bin/env python3

import sys
from secret import Hmac

from helpers import eprint, generate_check_url
from game import Game
from menu import Menu, MenuItem
from table import show_table


def main():
    hmac = Hmac()
    params = sys.argv[1:]
    if len(params) < 3:
        eprint("Not enough arguments")

    if len(params) % 2 == 0:
        eprint("There must be an odd number of arguments")

    if len(params) != len(set(params)):
        eprint("Arguments must be different")

    game = Game(moves=params)
    result = game.generate_result_function("Draw", "You win!", "Computer win!")

    menu_action = None
    menu_items = (
        [MenuItem(str(i), val, menu_action) for i, val in enumerate(game.moves, 1)]
        + [MenuItem("0", "exit", None)]
        + [MenuItem("?", "help", None)]
    )

    menu = Menu(menu_items, header="Available moves:")

    while True:
        message, c_move = game.generate_computer_move()
        hmac_code = hmac.calc(message)
        print(f"HMAC: {hmac_code}")

        print(menu.generate_menu())

        ans = input("Enter your move: ")
        if ans == "0":
            print(f"key = {hmac.secret}")
            print(generate_check_url(hmac.secret, game.computer_moves))
            break

        if ans == "?":
            show_table(game)
            continue

        umi = int(ans) - 1
        print(f"Your move: {params[umi]}")
        print(f"Computer move: {c_move}")
        print(f"{result(umi, c_move)}")

        print("*" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ncya")
