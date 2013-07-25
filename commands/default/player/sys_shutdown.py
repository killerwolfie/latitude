from ev import default_cmds

class CmdSysShutdown(default_cmds.CmdShutdown):
    """
    @shutdown - Stop the server and portal

    Usage:
      @shutdown [announcement]
        Gracefully shut down both Server and Portal.
    """
    key = "@shutdown"
    locks = "cmd:perm(commandy_@shutdown) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

