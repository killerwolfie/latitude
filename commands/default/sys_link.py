from ev import default_cmds

class CmdSysLink(default_cmds.CmdLink):
    """
    @link - connect objects

    Usage:
      @link[/switches] <object> = <target>
      @link[/switches] <object> =
      @link[/switches] <object>

    Switch:
      twoway - connect two exits. For this to work, BOTH <object>
               and <target> must be exit objects.

    If <object> is an exit, set its destination to <target>. Two-way operation
    instead sets the destination to the *locations* of the respective given
    arguments.
    The second form (a lone =) sets the destination to None (same as the @unlink command)
    and the third form (without =) just shows the currently set destination.
    """

    key = "@link"
    locks = "cmd:pperm(link) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

