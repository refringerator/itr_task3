from string import Template
from collections import namedtuple
from functools import reduce

MenuItem = namedtuple("MenuItem", ["key", "description", "action"])


class Menu:
    def __init__(self, items: list[MenuItem], header="", template="") -> None:
        if not template:
            template = "$key - $description"
        self.template = Template(template)
        self.items = items
        self.header = header

    def generate_menu(self) -> str:
        sub = self.template.safe_substitute
        menu_lines = [sub(item._asdict()) for item in self.items]
        if self.header:
            menu_lines.insert(0, self.header)
        return "\n".join(menu_lines)

    def check_input(self, input: str) -> bool:
        return input in [item.key for item in self.items]

    def select(self, text):
        print(self.generate_menu())
        user_input = input(text)
        while not self.check_input(user_input):
            print("Invalid input!")
            return self.select(text)

        return reduce(
            lambda x, el: el.action if el.key == user_input and el.action else x,
            self.items,
            user_input,
        )
