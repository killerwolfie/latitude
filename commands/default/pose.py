from game.gamesrc.latitude.commands.default import say

class CmdPose(say.CmdSay):
    """
    pose - strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """

    key = "pose"
    aliases = [':']
    locks = "cmd:all()"
    help_category = "Actions"

    def func(self):
        message = self.gen_pose(self.args)
        if self.caller.location:
            # Call the speech hook on the location
            self.caller.location.at_say(self.caller, message)
            self.caller.location.msg_contents(message, data={"raw":True})
        else:
            self.caller.msg(message, data={"raw":True})

