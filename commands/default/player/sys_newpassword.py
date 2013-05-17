from ev import default_cmds

class CmdSysNewPassword(default_cmds.CmdNewPassword):
    """
    @newpassword

    Usage:
      @newpassword <user obj> = <new password>

    Set a player's password.
    """

    key = "@newpassword"
    aliases = []
    locks = "cmd:pperm(command_@newpassword) or pperm(Janitors)"
    help_category = "=== Admin ==="

