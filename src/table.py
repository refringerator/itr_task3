from prettytable import PrettyTable
from game import Game


def show_table(game: Game):
    table = PrettyTable()
    table.field_names = ["v User \\ PC >", *game.moves]

    res = game.generate_result_function("Draw", "Win", "Lose")
    for row_move in game.moves:
        table.add_row([row_move, *[res(row_move, col_move) for col_move in game.moves]])

    print("Table shows your result")
    print(table)
