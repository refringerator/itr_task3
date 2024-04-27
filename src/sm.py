from typing import Any
from statemachine import State
from statemachine import StateMachine

from game import Game


class InteractMachine(StateMachine):
    start = State(initial=True)
    show_info = State()
    round = State()
    help = State()
    finish = State(final=True)

    begin = start.to(show_info)

    input = (
        show_info.to(help, cond="help")
        | show_info.to(finish, cond="exit")
        | show_info.to(round, cond="move")
    )

    auto = round.to(show_info) | help.to(show_info)

    def __init__(
        self,
        input_function,
        model: Any = None,
        state_field: str = "state",
        start_value: Any = None,
        rtc: bool = True,
        allow_event_without_transition: bool = False,
    ):
        super().__init__(
            model, state_field, start_value, rtc, allow_event_without_transition
        )
        self.input_function = input_function

    def on_enter_help(self):
        self.send("auto")

    def on_enter_round(self):
        self.send("auto")

    def run(self):
        self.send("begin")

        while not self.current_state.final:
            self.send("input", self.input_function())


class Engine:
    HELP = "HELP ANSWER"
    EXIT = "END ANSWER"

    def __init__(
        self,
        game: Game,
        help_action=None,
        finish_action=None,
        round_action=None,
        show_info_action=None,
    ):
        self.game = game
        self.help_action = self.prepare_function(help_action)
        self.finish_action = self.prepare_function(finish_action)
        self.round_action = self.prepare_function(round_action)
        self.show_info_action = self.prepare_function(show_info_action)

    @staticmethod
    def prepare_function(func):
        if not func:
            return lambda *args: None
        return func

    def on_enter_help(self):
        self.help_action(self.game)

    def on_enter_finish(self):
        self.finish_action()

    def on_enter_round(self):
        self.round_action(self.game.last_user_move, self.game)
        self.game.finish_round()

    def on_exit_round(self):
        self.game.show_round_result()

    def on_enter_show_info(self):
        self.show_info_action(self.game)

    def move(self, ans):
        self.game.set_last_user_move(ans)
        return True

    def help(self, ans):
        return ans == self.HELP

    def exit(self, ans):
        return ans == self.EXIT
