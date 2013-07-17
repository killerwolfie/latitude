from game.gamesrc.latitude.commands.default.character import look

class CmdInventory(look.CmdLook):
    """
    inventory - Look at contents

    Usage:
      inventory
        Show the items you're holding, and associated information.

      look inside <object>
      inventory <object>
        Look inside an object and display its contents.
    """
    key = "inventory"
    aliases = ["inv", "look inside"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        if self.cmdstring.lower() == 'look inside' and not self.args:
            self.msg('Look inside what?')
            return
        if self.cmdstring.lower() == 'look inside' and self.args.lower() in ['me', 'self']:
            self.msg("You probe the very depths of your soul.  Unfathomable truths are realized.  \"Dear god.  I'm a character in some kind of game!!\"")
            return
        self.percieve('contents', default_obj=self.character)

