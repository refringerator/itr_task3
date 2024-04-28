#!/usr/bin/env python3

import sys
import os

from helpers import check_params, generate_check_url
from game import Game
from menu import Menu, MenuItem
from table import show_table
from sm import InteractMachine, Engine

import time
from rich import print as rich_print


def delayed_rich_print(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    lines = sep.join([str(arg) for arg in args]).split("\n")
    for line in lines:
        time.sleep(os.getenv("SLEEP", 0.05))
        rich_print(line, **kwargs)


__builtins__.print = delayed_rich_print


def main(params: list[str]):
    game = Game(moves=params)
    game.result_function = game.generate_result_function(
        "[bold yellow]Draw[/]",
        "[magenta bold]Computer win![/]",
        "[green bold]You win![/]",
    )

    engine = Engine(
        game,
        help_action=show_table,
        finish_action=lambda: print(
            f"\nHere is the HMAC key that was used during the game: [bold purple4]{game.get_secret()}[/]\n"
            f"You can check HMAC for computer's moves on the following website\n"
            f"{generate_check_url(game.get_secret(), game.get_computer_moves())}"
        ),
    )

    menu = Menu(
        header="[bold underline]Available moves:[/]",
        items=(
            [MenuItem(str(i), val, val) for i, val in enumerate(game.moves, 1)]
            + [MenuItem("0", "exit", Engine.EXIT)]
            + [MenuItem("?", "help", Engine.HELP)]
        ),
        template="[bold blue]$key[/] - [italic bold]$description[/]",
        error_message="[bold red]Invalid input![/]",
    )

    def input_function():
        return menu.select("Enter your move: ")

    sm = InteractMachine(input_function, engine)
    sm.run()


if __name__ == "__main__":
    check_params(params := sys.argv[1:])

    try:
        main(params)
    except KeyboardInterrupt:
        print("\ncya")
