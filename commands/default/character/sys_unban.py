from ev import default_cmds

class CmdSysUnban(default_cmds.CmdUnban):
    """
    remove a ban

    Usage:
      @unban <banid>

    This will clear a player name/ip ban previously set with the @ban
    command.  Use this command without an argument to view a numbered
    list of bans. Use the numbers in this list to select which one to
    unban.

    """
    key = "@unban"
    locks = "cmd:perm(command_@unban) or perm(Janitors)"
    help_category="=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

