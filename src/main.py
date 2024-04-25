#!/usr/bin/env python3

import sys
from secret import generate_secret_key, calc_hmac
import random
from helpers import eprint, generate_check_url
from game import Game
from menu import show_menu
from table import show_table


def main():
    computer_moves = []
    secret = generate_secret_key()
    params = sys.argv[1:]
    if len(params) < 3:
        eprint("Not enough arguments")

    if len(params) % 2 == 0:
        eprint("There must be an odd number of arguments")

    if len(params) != len(set(params)):
        eprint("Arguments must be different")

    game = Game(moves=params)

    n = 0
    while True:
        # random move
        n += 1
        move = random.choice(params)
        cmi = params.index(move)
        message = f"{n}) {move}"
        computer_moves.append(message)

        hmac = calc_hmac(secret, message)
        print(f"HMAC: {hmac}")

        show_menu(params)

        ans = input("Enter your move: ")
        if ans == "0":
            print(f"key = {secret}")
            print(generate_check_url(secret, computer_moves))
            break

        if ans == "?":
            show_table(params)
            continue

        umi = int(ans) - 1
        print(f"Your move: {params[umi]}")
        print(f"Computer move: {params[cmi]}")

        r = game.check_winner(umi, cmi)

        if r == 0:
            gg = "Draw"
        elif r > 0:
            gg = "Computer win!"
        elif r < 0:
            gg = "You win!"

        print(f"{gg}")

        print(f"Comp {cmi}, user {umi}, result={r}")
        print("*" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ncya")
