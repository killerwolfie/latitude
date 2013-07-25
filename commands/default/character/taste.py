from game.gamesrc.latitude.commands.default.character import look

class CmdTaste(look.CmdLook):
    """
    taste - Use your sense of taste

    Usage:
      taste
      taste <obj>
        Licks your general environment, or objects in your vicinity to examine flavors.
    """
    key = "taste"
    aliases = ["lick"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('flavor')
