from ev import default_cmds

class CmdSysChannelCreate(default_cmds.CmdChannelCreate):
    """
    @ccreate - Create a new channel

    Usage:
      channelcreate
      @ccreate <new channel>[;alias;alias...] = description
        Creates a new channel owned by you.
    """

    key = "@ccreate"
    aliases = "channelcreate"
    locks = "cmd:perm(command_@ccreate) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

