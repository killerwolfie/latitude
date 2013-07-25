from ev import default_cmds

class CmdSysReset(default_cmds.CmdReset):
    """
    @reset - Reset and reboot the system

    Usage:
      @reset
        A cold reboot. This works like a mixture of @reload and @shutdown.  All
        shutdown hooks will be called and non-persistent scrips will be purged,
        but the Portal will not be affected and the server will automatically
        restart again.
    """
    key = "@reset"
    aliases = []
    locks = "cmd:perm(command_@reset) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

