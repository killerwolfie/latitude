from ev import default_cmds

class CmdSysCdestroy(default_cmds.CmdCdestroy):
    """
    @cdestroy

    Usage:
      @cdestroy <channel>

    Destroys a channel that you control.
    """

    key = "@cdestroy"
    help_category = "Comms"
    locks = "cmd: not pperm(channel_banned)"

