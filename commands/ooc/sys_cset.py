from ev import default_cmds

class CmdSysCset(default_cmds.CmdCset):
    """
    @cset - changes channel access restrictions

    Usage:
      @cset <channel> [= <lockstring>]

    Changes the lock access restrictions of a channel. If no
    lockstring was given, view the current lock definitions.
    """

    key = "@cset"
    locks = "cmd:not pperm(channel_banned)"
    aliases = ["@cclock"]
    help_category = "Comms"

