from ev import default_cmds

class CmdLook(default_cmds.MuxPlayerCommand):
    """
    look

    Usage:
      look
      look ['at'] <obj>

    Visually observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ['l']
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        if self.args:
            self.msg("There's nothing specific here to look at here.")
        else:
            self.msg(self.character.location.return_appearance())
