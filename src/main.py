#!/usr/bin/env python3

import sys
from secret import generate_secret_key, calc_hmac

from helpers import eprint, generate_check_url
from game import Game
from menu import show_menu
from table import show_table


def main():
    secret = generate_secret_key()
    params = sys.argv[1:]
    if len(params) < 3:
        eprint("Not enough arguments")

    if len(params) % 2 == 0:
        eprint("There must be an odd number of arguments")

    if len(params) != len(set(params)):
        eprint("Arguments must be different")

    game = Game(moves=params)

    while True:
        message, c_move = game.generate_computer_move()
        hmac = calc_hmac(secret, message)
        print(f"HMAC: {hmac}")

        show_menu(game.moves)

        ans = input("Enter your move: ")
        if ans == "0":
            print(f"key = {secret}")
            print(generate_check_url(secret, game.computer_moves))
            break

        if ans == "?":
            show_table(game)
            continue

        umi = int(ans) - 1
        print(f"Your move: {params[umi]}")
        print(f"Computer move: {c_move}")

        r = game.check_winner(umi, c_move)

        if r == 0:
            gg = "Draw"
        elif r > 0:
            gg = "Computer win!"
        elif r < 0:
            gg = "You win!"

        print(f"{gg}")

        print("*" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ncya")
