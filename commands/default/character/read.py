from game.gamesrc.latitude.commands.default.character import look

class CmdRead(look.CmdLook):
    """
    read - Read something

    Usage:
      read
      read <obj>
        Examine any writing that may be on your location or objects in your vicinity.
    """
    key = "read"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('writing')
