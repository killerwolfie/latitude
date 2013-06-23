from game.gamesrc.latitude.scripts.prompt_state import PromptState

class PromptLeave(PromptState):
    def option_y(self):
        self.db.prompt_finish_cmds = ['leave now']
        return None

    def option_n(self):
        self.obj.msg('You decide to stay where you are.')
        return None

    def show_options(self):
        self.obj.msg('Are you sure you want to leave the area? (y/n)')
