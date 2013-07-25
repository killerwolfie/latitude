from game.gamesrc.latitude.commands.default.character import look

class CmdListen(look.CmdLook):
    """
    listen - Use your sense of hearing

    Usage:
      listen
      listen <obj>
        Examine the sound of your location or objects in your vicinity.
    """
    key = "listen"
    aliases = ["hear", "listen to"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('sound')
