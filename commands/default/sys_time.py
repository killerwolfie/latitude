from ev import default_cmds

class CmdSysTime(default_cmds.CmdTime):
    """
    @time

    Usage:
      @time

    Server local time.
    """
    key = "@time"
    aliases = "@uptime"
    locks = "cmd:perm(time) or perm(Players)"
    help_category = "System"

