from ev import default_cmds

class CmdSysCdestroy(default_cmds.CmdCdestroy):
    """
    @cdestroy

    Usage:
      @cdestroy <channel>

    Destroys a channel that you control.
    """

    key = "@cdestroy"
    help_category = "--- Coder/Sysadmin ---"
    locks = "cmd:pperm(command_sys_cdestroy) or pperm(Custodians)"

