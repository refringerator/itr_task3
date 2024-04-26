from statemachine import State
from statemachine import StateMachine


class InteractMachine(StateMachine):
    start = State(initial=True)
    show_info = State()
    help = State()
    finish = State(final=True)

    begin = start.to(show_info)

    input = (
        show_info.to(help, cond="help")
        | show_info.to(finish, cond="exit")
        | show_info.to(show_info, cond="move")
    )

    auto = help.to(show_info)

    def on_enter_help(self):
        self.send("auto")

    def run(self):
        self.send("begin")

    def ppp(self):
        self.send("begin")


class Lol:
    HELP = "HELP ANSWER"
    EXIT = "END ANSWER"

    def __init__(self, help_action=None):
        self.ans = ""
        self.help_action = help_action

    def on_enter_help(self):
        if self.help_action:
            self.help_action()

    def move(self, ans):
        self.ans = ans
        return True

    def help(self, ans):
        self.ans = ans
        return ans == self.HELP

    def exit(self, ans):
        self.ans = ans
        return ans == self.EXIT
