from ev import default_cmds

class CmdSysHelp(default_cmds.CmdHelp):
    """
    @help - Get documentation on topics or commands

    Usage:
      @help
      @help list
      @help all
        List all available commands, and help topics.

      @help <command>
        Get help information associated with a command.

      @help <topic>
        Display specific help topic information.
    """
    key = '@help'
    aliases = [ 'help' ]
    locks = "cmd:all()"
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"
