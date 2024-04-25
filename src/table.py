from prettytable.colortable import ColorTable, Themes
from game import Game


def show_table(game: Game):
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["v PC \\ User >", *game.moves]

    def res(p):
        if p == 0:
            return "Draw"
        if p > 0:
            return "Lose"
        if p < 0:
            return "Win"

    for move in game.moves:
        table.add_row([move, *[res(game.check_winner(move, m)) for m in game.moves]])

    print("Table shows your result")
    print(table)
