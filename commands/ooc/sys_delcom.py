from ev import default_cmds

class CmdSysDelCom(default_cmds.CmdDelCom):
    """
    delcom - unsubscribe from channel or remove channel alias

    Usage:
       delcom <alias or channel>

    If the full channel name is given, unsubscribe from the
    channel. If an alias is given, remove the alias but don't
    unsubscribe.
    """

    key = "delcom"
    aliases = ["delaliaschan, delchanalias"]
    help_category = "Comms"
    locks = "cmd:not perm(channel_banned)"

