from game.gamesrc.latitude.commands.default.character import look

class CmdSmell(look.CmdLook):
    """
    smell

    Usage:
      smell
      smell <obj>

    Used to examine the scent of your location or objects in your vicinity.
    """
    key = "smell"
    aliases = ["sniff"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('scent')
