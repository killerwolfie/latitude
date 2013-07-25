from ev import default_cmds

class CmdSysCBoot(default_cmds.CmdCBoot):
    """
    @cboot - Kick a player from a channel you control.

    Usage:
      @cboot[/quiet] <channel> = <player> [:reason]
        Kicks a player or object from a channel you control.

    Switches:
      quiet
        Don't notify the channel
    """

    key = "@cboot"
    locks = "cmd:perm(command_@cboot) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

