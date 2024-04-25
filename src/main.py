#!/usr/bin/env python3

import sys
from secret import generate_secret_key, calc_hmac
import random
import urllib.parse
from game import check_winner
from menu import show_menu
from table import show_table


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print("Usage example: python", sys.argv[0], "rock", "paper", "scissors")
    sys.exit(1)


def main():
    computer_moves = []
    secret = generate_secret_key()
    params = sys.argv[1:]
    if len(params) < 3:
        eprint('Not enough arguments')

    if len(params) % 2 == 0:
        eprint("There must be an odd number of arguments")

    if len(params) != len(set(params)):
        eprint("Arguments must be different")


    n = 0
    while True:
        # random move
        n += 1
        move = random.choice(params)
        cmi = params.index(move)
        message = f"{n}) {move}"
        computer_moves.append(message)

        hmac = calc_hmac(secret, message)
        # print(hmac, message, cmi)
        print(f"HMAC: {hmac}")

        show_menu(params)

        ans = input("Enter your move: ")
        if ans == '0':
            print(f"key = {secret}")
            params = {
                'key': secret,
                'messages': ','.join(computer_moves)
            }
            k = urllib.parse.urlencode(params)
            resource = 'https://refringerator.github.io/itr_task3'
            link = f"{resource}/?{k}"
            print(link)
            break

        if ans == '?':
            show_table(params)
            continue

        umi = int(ans)-1
        print(f"Your move: {params[umi]}")
        print(f"Computer move: {params[cmi]}")
        
        r = check_winner(params, umi, cmi)

        if r == 0:
            gg = 'Draw'
        elif r>0:
            gg = 'Computer win!'
        elif r<0:
            gg = 'You win!'

        print(f"{gg}")

        print(f"Comp {cmi}, user {umi}, result={r}")
        print('*'*50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ncya")

