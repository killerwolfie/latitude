from game.gamesrc.latitude.commands.default.character import say

class CmdSpoof(say.CmdSay):
    """
    spoof - Allows you to make a freeform pose to the room.
    Usage:
      spoof <freeform text>

    Example (If your username is Tom):
      spoof The parade has started! [Tom]
    """
    key = "spoof"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []

    def func(self):
        message = '%ch%cw( %cn' + self.args.replace('%', '%%').replace('{', '{{') + '%ch%cw )'
        if self.caller.location:
            # Call the speech hook on the location
            self.caller.location.at_say(self.caller, message)
            self.caller.location.msg_contents(message)
        else:
            self.caller.msg(message)
