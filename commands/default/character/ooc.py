from game.gamesrc.latitude.commands.default.character import say

class CmdOOC(say.CmdSay):
    """
    ooc - Speak or pose with an Out of Character marker.
    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      ooc Hello, there!
       -> others will see:
      (OOC) Tom says, "Hello, there!"
    Example 2:
      ooc :waves.
       -> others will see:
      (OOC) Tom waves.

    Prepend OOC to a pose or statment.
    """
    key = "ooc"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []

    def func(self):
        if self.args.startswith(':'):
            message = self.gen_pose(self.args[1:])
        elif self.args.startswith('"'):
            message = self.gen_say(self.args[1:])
        else:
            message = self.gen_say(self.args)
        message = '{w<{rOOC{w> {n' + message
        if self.caller.location:
            # Call the speech hook on the location
            self.caller.location.at_say(self.caller, message)
            self.caller.location.msg_contents(message)
        else:
            self.caller.msg(message)

