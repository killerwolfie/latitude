from ev import default_cmds

class CmdSysCset(default_cmds.CmdCset):
    """
    @cset - Changes channel access restrictions

    Usage:
      @cset <channel> [= <lockstring>]
        Changes the lock access restrictions of a channel. If no lockstring was
        given, view the current lock definitions.
    """

    key = "@cset"
    locks = "cmd:perm(command_@cset) or perm(Janitors)"
    aliases = []
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

