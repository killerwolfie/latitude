from ev import default_cmds

class CmdSysCset(default_cmds.CmdCset):
    """
    @cset - changes channel access restrictions

    Usage:
      @cset <channel> [= <lockstring>]

    Changes the lock access restrictions of a channel. If no
    lockstring was given, view the current lock definitions.
    """

    key = "@cset"
    locks = "cmd:perm(command_@cset) or perm(Custodians)"
    aliases = []
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

