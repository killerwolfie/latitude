from ev import default_cmds

class CmdSysChannelCreate(default_cmds.CmdChannelCreate):
    """
    @ccreate
    channelcreate
    Usage:
     @ccreate <new channel>[;alias;alias...] = description

    Creates a new channel owned by you.
    """

    key = "@ccreate"
    aliases = "channelcreate"
    locks = "cmd:pperm(command_sys_ccreate) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

