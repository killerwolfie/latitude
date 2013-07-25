from ev import default_cmds

class CmdPose(default_cmds.MuxPlayerCommand):
    """
    pose - Strike a pose

    Usage:
      pose <pose text>
      :<pose text>
        Describe an action being taken. The pose text will automatically begin
        with your name.  This is used to communicate an 'action' to other players,
        and you can use it in roleplaying!

    Example:
      pose is standing by the wall, smiling.
        (Others will see:) <Your name> is standing by the wall, smiling.

    See {whelp Roleplaying{n for more information.
    """

    key = "pose"
    aliases = [':', ';']
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

