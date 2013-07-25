from ev import default_cmds

class CmdSysCdesc(default_cmds.CmdCdesc):
    """
    @cdesc - Set channel description

    Usage:
      @cdesc <channel> = <description>
        Changes the description of the channel as shown in channel lists.
    """

    key = "@cdesc"
    locks = "cmd:perm(command_@cdesc) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

