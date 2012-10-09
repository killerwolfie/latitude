from game.gamesrc.latitude.commands.default import look

class CmdRead(look.CmdLook):
    """
    listen

    Usage:
      listen
      listen <obj>

    Used to examine any writing that may be on your location or objects in your vicinity.
    """
    key = "read"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('writing')
