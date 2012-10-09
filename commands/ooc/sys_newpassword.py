from ev import default_cmds

class CmdSysNewPassword(default_cmds.CmdNewPassword):
    """
    @setpassword

    Usage:
      @userpassword <user obj> = <new password>

    Set a player's password.
    """

    key = "@userpassword"
    locks = "cmd:pperm(newpassword) or pperm(Janitors)"
    help_category = "=== Admin ==="

