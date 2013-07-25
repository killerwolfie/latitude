from ev import default_cmds

class CmdSpoof(default_cmds.MuxPlayerCommand):
    """
    spoof - Make a freeform pose to the room
    
    Allows you to make a freeform pose to the room.

    Usage:
      spoof <freeform text>

    Example:
      spoof The parade has started!
        -> (others will see:) The parade has started! (<Your name>)
    """
    key = "@spoof"
    locks = "cmd:all()"
    help_category = "Communication"
    aliases = ['spoof', '|']
#    arg_regex = r"\s.*?|$"

    def func(self):
        message = self.args.replace('%', '%%').replace('{', '{{') + ' %cn%cb(' + self.character.name + ')'
        if self.character.location:
            # Call the speech hook on the location
            self.character.location.at_say(self.character, message)
            self.character.location.msg_contents(message)
        else:
            self.character.msg(message)
