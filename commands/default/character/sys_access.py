from ev import default_cmds

class CmdSysAccess(default_cmds.CmdAccess):
    """
    access - show access groups

    Usage:
      @access

    This command shows you the permission hierarchy and
    which permission groups you are a member of.
    """
    key = "@access"
    locks = "cmd:all()"
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"
