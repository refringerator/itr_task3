import math


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
