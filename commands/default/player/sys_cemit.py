from ev import default_cmds

class CmdSysCemit(default_cmds.CmdCemit):
    """
    @cemit - Send a message to channel

    Usage:
      @cemit[/switches] <channel> = <message>
        Allows the user to broadcast a message over a channel as long as they
        control it. It does not show the user's name unless they provide the
        /sendername switch.

    Switches:
      noheader
        Don't show the [channel] header before the message

      sendername
        Attach the sender's name before the message

      quiet
        Don't echo the message back to sender
    """

    key = "@cemit"
    aliases = []
    locks = "cmd:perm(command_@cemit) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

