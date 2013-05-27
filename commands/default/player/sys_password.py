from ev import default_cmds

class CmdSysPassword(default_cmds.CmdPassword):
    """
    @password - set your password

    Usage:
      @password <old password> = <new password>

    Changes your password. Make sure to pick a safe one.
    """
    key = "@password"
    locks = "cmd:all()"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

