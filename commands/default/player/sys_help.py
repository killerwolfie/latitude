from ev import default_cmds

class CmdSysHelp(default_cmds.CmdHelp):
    """
    The main help command

    Usage:
      help <topic or command>
      help list
      help all

    This will search for help on commands and other
    topics related to the game.
    """
    key = '@help'
    aliases = [ 'help' ]
    locks = "cmd:all()"
    arg_regex = r"(/\w+?(\s|$))|\s|$"
