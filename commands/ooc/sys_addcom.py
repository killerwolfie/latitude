from ev import default_cmds

class CmdSysAddCom(default_cmds.CmdAddCom):
    """
    addcom - subscribe to a channel with optional alias

    Usage:
       addcom [alias=] <channel>

    Joins a given channel. If alias is given, this will allow you to
    refer to the channel by this alias rather than the full channel
    name. Subsequent calls of this command can be used to add multiple
    aliases to an already joined channel.
    """

    key = "addcom"
    aliases = ["aliaschan","chanalias"]
    help_category = "Comms"
    locks = "cmd:not pperm(channel_banned)"

