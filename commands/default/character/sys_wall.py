from ev import default_cmds

class CmdSysWall(default_cmds.CmdWall):
    """
    @wall

    Usage:
      @wall <message>

    Announces a message to all connected players.
    """
    key = "@wall"
    locks = "cmd:pperm(command_@wall) or pperm(Janitors)"
    help_category = "=== Admin ==="

