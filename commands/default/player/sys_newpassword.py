from ev import default_cmds

class CmdSysNewPassword(default_cmds.CmdNewPassword):
    """
    @newpassword - Set player password

    Usage:
      @newpassword <player> = <new password>
        Set a player's password.
    """

    key = "@newpassword"
    aliases = []
    locks = "cmd:perm(command_@newpassword) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

