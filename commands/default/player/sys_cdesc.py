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
    locks = "cmd:pperm(command_sys_cdesc) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

