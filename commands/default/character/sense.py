from game.gamesrc.latitude.commands.default.character import look

class CmdSense(look.CmdLook):
    """
    sense 

    Usage:
      sense
      sense <obj>

    Used to examine the aura of your location or objects in your vicinity.
    """
    key = "sense"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('aura')
