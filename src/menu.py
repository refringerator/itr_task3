from string import Template
from collections import namedtuple


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
