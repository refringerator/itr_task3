from prettytable import PrettyTable
from rich.table import Table
from rich.console import Console
from itertools import cycle


def show_table(game):
    table = PrettyTable()
    table.field_names = ["v PC \\ User >", *game.moves]

    res = game.generate_result_function("Draw", "Lose", "Win")
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
