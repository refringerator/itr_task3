def show_menu(params):
    print("Available moves:")
    for i,v in enumerate(params, 1):
        print(f"{i} - {v}")

    print("0 - exit")
    print("? - help")
