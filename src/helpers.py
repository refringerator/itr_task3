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
    print(*args, file=sys.stderr, **kwargs)
    print("Usage example: python", sys.argv[0], "rock", "paper", "scissors")
    sys.exit(1)
