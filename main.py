# доки https://hmacgenerator.com/
# https://pypi.org/project/prettytable/
# https://rich.readthedocs.io/en/stable/introduction.html

import sys
import hashlib
import secrets
import hmac
import math


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    print("Usage example: python", sys.argv[0], "rock", "paper", "scissors")
    sys.exit(1)


def check_winner(params, a: int, b: int) -> int:
    n = len(params)
    if a>=n or b>=n or a<0 or b<0:
        raise IndexError("Index out of range")

    p = math.floor(n / 2)
    return (a - b + p + n) % n - p;


def main():
    params = sys.argv[1:]
    if len(params) < 3:
        eprint('Not enough arguments')

    if len(params) % 2 == 0:
        eprint("There must be an odd number of arguments")

    if len(params) != len(set(params)):
        eprint("Arguments must be different")

    secret = secrets.token_urlsafe(16)
    message = 'my message'.encode()
    hmac_msg = hmac.new(secret.encode(), message, hashlib.sha3_256).hexdigest()
    print('it works', params)
    print(hmac_msg)
    print(message, secret, secrets.token_hex(16))


if __name__ == "__main__":
    main()

