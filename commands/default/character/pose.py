from ev import default_cmds

class CmdPose(default_cmds.MuxPlayerCommand):
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
#    arg_regex=r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        message = self.character.speech_pose(self.args)
        if self.character.location:
            # Call the speech hook on the location
            self.character.location.at_say(self.character, message)
            self.character.location.msg_contents(message)
        else:
            self.msg(message)

