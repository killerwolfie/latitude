from ev import default_cmds

class CmdSysOOCLook(default_cmds.CmdOOCLook):
    """
    ooc look

    Usage:
      look

    This is an OOC version of the look command. Since a
    Player doesn't have an in-game existence, there is no
    concept of location or "self". If we are controlling
    a character, pass control over to normal look.

    """

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    help_category = "General"

