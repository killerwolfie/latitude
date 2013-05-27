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
    locks = "cmd:perm(command_@newpassword) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

