from game.gamesrc.latitude.commands.default.character import say

class CmdSysOOCSay(say.CmdSay):
    """
    @oocsay - Speak or pose with an Out of Character marker.
    Use this to make sure people can tell you're not roleplaying.

    Usage:
        @oocsay <text>
        @oocsay :<pose>

    Example:
      @oocsay Hello, there!
       -> others will see:
      <OOC> Tom says, "Hello, there!"

    Example 2:
      @oocsay :waves.
       -> others will see:
      <OOC> Tom waves.
    """
    key = "@oocsay"
    locks = "cmd:all()"
    help_category = "General"
    aliases = ['ooc']
    arg_regex = r"\s.*?|$"

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

