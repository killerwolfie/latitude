from ev import default_cmds

class CmdSysReload(default_cmds.CmdReload):
    """
    @reload - Reload the system

    Usage:
      @reload
        This restarts the server. The Portal is not affected. Non-persistent
        scripts will survive a @reload (use @reset to purge) and at_reload() hooks
        will be called.
    """
    key = "@reload"
    locks = "cmd:perm(command_@reload) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

