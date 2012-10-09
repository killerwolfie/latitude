from game.gamesrc.latitude.commands.default import look

class CmdTaste(look.CmdLook):
    """
    taste

    Usage:
      taste
      taste <obj>

    Licks your general environment, or objects in your vicinity to get examine your flavor.
    """
    key = "taste"
    aliases = ["lick"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('flavor')
