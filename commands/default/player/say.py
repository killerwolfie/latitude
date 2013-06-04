from ev import default_cmds

class CmdSay(default_cmds.MuxPlayerCommand):
    """
    say

    OOC version of the 'say' command
    """
    key = "say"
    aliases = ['"']
    locks = "cmd:all()"
    help_category = "Actions"
    auto_help = False

    def func(self):
        self.msg("{RYou're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R.")
