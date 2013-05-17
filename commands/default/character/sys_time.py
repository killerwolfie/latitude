from ev import default_cmds

class CmdSysTime(default_cmds.CmdTime):
    """
    @time

    Usage:
      @time

    Server local time.
    """
    key = "@time"
    locks = "cmd:all()"
    help_category = "Information"

