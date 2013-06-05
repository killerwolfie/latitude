from ev import default_cmds

class CmdSysWall(default_cmds.CmdWall):
    """
    @wall

    Usage:
      @wall <message>

    Announces a message to all connected players.
    """
    key = "@wall"
    locks = "cmd:perm(command_@wall) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"
