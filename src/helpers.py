import urllib.parse
import sys
import os


def generate_check_url(key: str, computer_moves: list[str]) -> str:
    search_params = {
        "key": key,
        "messages": ",".join(computer_moves),
    }
    encoded_params = urllib.parse.urlencode(search_params)
    resource = os.getenv("CHECK_URL", "https://refringerator.github.io/itr_task3")
    url = f"{resource}{'' if resource.endswith('/') else '/'}?{encoded_params}"
    return url


def eprint(*args, **kwargs):
    print("[red bold]", *args, file=sys.stderr, **kwargs)
    print("[deep_sky_blue1]Usage example: python", sys.argv[0], "rock", "paper", "scissors")
    sys.exit(1)


def check_params(params):
    if len(params) < 3:
        eprint("Not enough arguments")

    if len(params) % 2 == 0:
        eprint("There must be an odd number of arguments")

    if len(params) != len(set(params)):
        eprint("Arguments must be different")
