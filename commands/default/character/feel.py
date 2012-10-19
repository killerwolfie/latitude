from game.gamesrc.latitude.commands.default.character import look

class CmdFeel(look.CmdLook):
    """
    feel

    Usage:
      feel
      feel <obj>

    Used to examine the texture of your location or objects in your vicinity.
    """
    key = "feel"
    aliases = ["touch"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('texture')
