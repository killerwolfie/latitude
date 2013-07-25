from ev import default_cmds

class CmdSysUnban(default_cmds.CmdUnban):
    """
    @unban - Remove a ban

    Usage:
      @unban
        View a numbered list of bans.

      @unban <banid>
        Using a number from the list of bans, clear the ban of the given player
        name/ip ban previously set with the @ban command.
    """
    key = "@unban"
    locks = "cmd:perm(command_@unban) or perm(Janitors)"
    help_category="=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

