from game.gamesrc.latitude.commands.default.character import say

class CmdSysSpoof(say.CmdSay):
    """
    spoof - Allows you to make a freeform pose to the room.
    Usage:
      spoof <freeform text>

    Example:
      spoof The parade has started!
      -> others will see:
      ( The parade has started! )
    """
    key = "@spoof"
    locks = "cmd:all()"
    help_category = "Communication"
    aliases = ['spoof']
    arg_regex = r"\s.*?|$"

    def func(self):
        message = '%ch%cw( %cn' + self.args.replace('%', '%%').replace('{', '{{') + '%ch%cw )'
        if self.caller.location:
            # Call the speech hook on the location
            self.caller.location.at_say(self.caller, message)
            self.caller.location.msg_contents(message)
        else:
            self.caller.msg(message)
