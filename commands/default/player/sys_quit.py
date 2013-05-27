from ev import default_cmds

class CmdSysQuit(default_cmds.CmdQuit):
    """
    quit

    Usage:
      @quit

    Gracefully disconnect from the game.
    """
    key = "@quit"
    locks = "cmd:all()"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

