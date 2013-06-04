from ev import default_cmds

class CmdPose(default_cmds.MuxPlayerCommand):
    """
    pose

    OOC version of the 'pose' command
    """
    key = "pose"
    aliases = [':']
    locks = "cmd:all()"
    help_category = "Actions"
    auto_help = False

    def func(self):
        self.msg("{RYou're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R.")
