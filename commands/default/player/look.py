from . import sys_char

class CmdLook(sys_char.CmdSysChar):
    """
    look

    OOC version of the 'look' command
    """
    key = "look"
    aliases = ['l']
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"
    auto_help = False

    def func(self):
        super(CmdLook, self).func()
