# доки https://hmacgenerator.com/
# https://pypi.org/project/prettytable/
# https://rich.readthedocs.io/en/stable/introduction.html

import sys
import hashlib
import secrets
import hmac


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        eprint('Not enough arguments')

    if len(sys.argv) % 2 == 1:
        eprint("There must be an odd number of arguments")

    secret = secrets.token_urlsafe(16)
    message = 'my message'.encode()
    hmac_msg = hmac.new(secret.encode(), message, hashlib.sha1).hexdigest()
    print('it works')
    print(hmac_msg)
    print(message, secret, secrets.token_hex(16))


if __name__ == "__main__":
    main()

