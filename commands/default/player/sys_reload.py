from ev import default_cmds

class CmdSysReload(default_cmds.CmdReload):
    """
    Reload the system

    Usage:
      @reload

    This restarts the server. The Portal is not
    affected. Non-persistent scripts will survive a @reload (use
    @reset to purge) and at_reload() hooks will be called.
    """
    key = "@reload"
    locks = "cmd:pperm(reload) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
