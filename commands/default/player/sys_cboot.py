from ev import default_cmds

class CmdSysCBoot(default_cmds.CmdCBoot):
    """
    @cboot

    Usage:
       @cboot[/quiet] <channel> = <player> [:reason]

    Switches:
       quiet - don't notify the channel

    Kicks a player or object from a channel you control.

    """

    key = "@cboot"
    locks = "cmd:perm(command_@cboot) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

