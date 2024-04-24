# доки https://hmacgenerator.com/
# https://pypi.org/project/prettytable/
# https://rich.readthedocs.io/en/stable/introduction.html

import sys
import hashlib
import random
import secrets
import hmac
import math
from prettytable.colortable import ColorTable, Themes


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print("Usage example: python", sys.argv[0], "rock", "paper", "scissors")
    sys.exit(1)


def show_table(params: list):
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["v PC \\ User >", *params]

    def res(p):
        if p==0: return "Draw"
        if p>0: return "Lose"
        if p<0: return "Win"

    for param in params:
        table.add_row([param, *[res(check_winner(params, param, p)) for p in params]])

    print("Table shows your result")
    print(table)


def check_winner(params: list, a: int|str, b: int|str) -> int:
    n = len(params)
    if isinstance(a, str):
        a = params.index(a)
    if isinstance(b, str):
        b = params.index(b)

    if a>=n or b>=n or a<0 or b<0:
        raise IndexError("Index out of range")

    p = math.floor(n / 2)
    return (a - b + p + n) % n - p


def calc_hmac(secret: str, message: str):
    return hmac.new(secret.encode(), message.encode(), hashlib.sha3_256).hexdigest()

def main():
    computer_moves = []
    secret = secrets.token_urlsafe(16)
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

        # show 
        print("Available moves:")
        for i,v in enumerate(params, 1):
            print(f"{i} - {v}")

        print("0 - exit")
        print("? - help")

        ans = input("Enter your move: ")
        if ans == '0':
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

