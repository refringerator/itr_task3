from prettytable import PrettyTable
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.console import Console
from itertools import cycle
import random

import time
from contextlib import contextmanager

from rich.live import Live


def show_table(game):
    table = PrettyTable()
    table.field_names = ["v PC \\ User >", *game.moves]

    res = game.wd.generate_result_function("Draw", "Lose", "Win")
    for row_move in game.moves:
        table.add_row([row_move, *[res(row_move, col_move) for col_move in game.moves]])

    print("Table shows your result")
    print(table)


def show_rich_table(caption, title, columns, rows):
    colors = ["cyan", "magenta", "green"]
    table = Table(title=title, caption=caption)

    for column, color in zip(columns, cycle(colors)):
        table.add_column(column, justify="left", style=color, no_wrap=True)

    for row in rows:
        table.add_row(*row)

    console = Console()
    console.print(table)


def show_interactive_help(game):
    console = Console()
    BEAT_TIME = 0.04

    @contextmanager
    def beat(length: int = 1):
        yield
        time.sleep(length * BEAT_TIME)

    def gt(columns, rows):
        table = Table(*columns)
        for row in rows:
            table.add_row(*row)
        return table

    def typing_effect(text: Text, message: str, end="\n", style=None):
        for char in message + end:
            with beat():
                text.append(char, style=style)

    columns = ["v PC \\ User >", *game.moves]
    res = game.wd.generate_result_function("Draw", "Lose", "Win")
    rows = [
        [row_move, *[res(row_move, col_move) for col_move in game.moves]]
        for row_move in game.moves
    ]

    layout = Layout()
    layout.split(
        Layout(name="table", size=len(rows) + 5),
        Layout(name="text"),
    )
    layout["table"].update(gt(columns, rows))

    text = Text("", style="bold")
    layout["text"].update(text)

    fr = game.get_finished_rounds()
    cm = fr[-1].computer_move if fr else random.choice(game.moves)
    pm = fr[-1].player_move if fr else random.choice(game.moves)

    res = res(cm, pm)
    col_index = game.moves.index(pm) + 1
    row_index = game.moves.index(cm)

    res_text = ("So the player ", f"{res}s") if res != "Draw" else ("It's", " Draw")

    with Live(layout, console=console, screen=True, refresh_per_second=20):
        with beat(10):
            typing_effect(
                text,
                "The table shows your score based on your move and the computer's move",
            )

        with beat(50):
            blink_rows = [[f"[blink]{r[0]}[/]"] + r[1:] for r in rows]
            layout["table"].update(gt(columns, rows=blink_rows))
            typing_effect(
                text, "The first column shows the possible moves of the computer"
            )

        with beat(50):
            blink_header = [columns[0]] + [f"[blink]{h}[/]" for h in columns[1:]]
            layout["table"].update(gt(columns=blink_header, rows=rows))
            typing_effect(
                text, "The table header shows the possible moves of the player"
            )

        with beat(30):
            layout["table"].update(gt(columns, rows))
            typing_effect(
                text,
                "At the intersection you can find the result of the round",
                end="\n\n",
            )

        with beat(30):
            typing_effect(text, "let's take an example")
        with beat(10):
            typing_effect(text, "Let's pretend the computer has chosen ", end="")
            typing_effect(text, cm, style="yellow4")
        with beat(50):
            rows[row_index][0] = f"[blink yellow4]{cm}[/]"
            layout["table"].update(gt(columns, rows))

        with beat(10):
            typing_effect(text, "And the player in turn chose ", end="")
            typing_effect(text, pm, style="yellow4")
        with beat(50):
            columns[col_index] = f"[blink yellow4]{pm}[/]"
            rows[row_index][0] = f"[yellow4]{cm}[/]"
            layout["table"].update(gt(columns, rows))
        with beat(10):
            typing_effect(text, res_text[0], end="")
            typing_effect(text, res_text[1], style="chartreuse2")
        with beat(50):
            columns[col_index] = f"[yellow4]{pm}[/]"
            rows[row_index][0] = f"[yellow4]{cm}[/]"
            rows[row_index][col_index] = f"[blink chartreuse2]{res}[/]"
            layout["table"].update(gt(columns, rows))
        with beat(50):
            columns[col_index] = f"[yellow4]{pm}[/]"
            rows[row_index][0] = f"[yellow4]{cm}[/]"
            rows[row_index][col_index] = f"[chartreuse2]{res}[/]"
            layout["table"].update(gt(columns, rows))

    table = gt(rows=[], columns=columns)
    with Live(table, console=console, screen=False, refresh_per_second=20):
        for row in rows:
            with beat(5):
                table.add_row(*row)
