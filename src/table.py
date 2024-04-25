from prettytable.colortable import ColorTable, Themes
from game import check_winner


def show_table(params: list):
    table = ColorTable(theme=Themes.OCEAN)
    table.field_names = ["v PC \\ User >", *params]

    def res(p):
        if p == 0:
            return "Draw"
        if p > 0:
            return "Lose"
        if p < 0:
            return "Win"

    for param in params:
        table.add_row([param, *[res(check_winner(params, param, p)) for p in params]])

    print("Table shows your result")
    print(table)
