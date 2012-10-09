from game.gamesrc.latitude.commands.default import look

class CmdListen(look.CmdLook):
    """
    listen

    Usage:
      listen
      listen <obj>

    Used to examine the sound of your location or objects in your vicinity.
    """
    key = "listen"
    aliases = ["hear", "listen to"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('sound')
