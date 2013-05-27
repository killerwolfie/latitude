from ev import default_cmds

class CmdSysCdesc(default_cmds.CmdCdesc):
    """
    @cdesc - set channel description

    Usage:
      @cdesc <channel> = <description>

    Changes the description of the channel as shown in
    channel lists.
    """

    key = "@cdesc"
    locks = "cmd:perm(command_@cdesc) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

