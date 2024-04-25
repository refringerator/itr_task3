from src.menu import Menu, MenuItem


def test_generation_one_item():
    action = None
    items = [MenuItem("1", "1", action), MenuItem("2", "2", action)]
    menu = Menu(items)

    assert "1 - 1\n2 - 2" == menu.generate_menu()


def test_generation_one_item_with_header():
    action = None
    items = [MenuItem("1", "1", action)]
    menu = Menu(items, header="hello")

    assert "hello\n1 - 1" == menu.generate_menu()


def test_generation_two_item_with_header():
    action = None
    items = [MenuItem("1", "1", action), MenuItem("2", "2", action)]
    menu = Menu(items, header="world")

    assert "world\n1 - 1\n2 - 2" == menu.generate_menu()
