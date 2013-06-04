from ev import default_cmds

class CmdSysCdestroy(default_cmds.CmdCdestroy):
    """
    @cdestroy

    Usage:
      @cdestroy <channel>

    Destroys a channel that you control.
    """

    key = "@cdestroy"
    help_category = "=== Admin ==="
    locks = "cmd:perm(command_@cdestroy) or perm(Janitors)"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

