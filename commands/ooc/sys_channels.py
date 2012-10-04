from ev import default_cmds

class CmdSysChannels(default_cmds.CmdChannels):
    """
    @clist

    Usage:
      @channels
      @clist
      comlist

    Lists all channels available to you, wether you listen to them or not.
    Use 'comlist" to only view your current channel subscriptions.
    """
    key = "@channels"
    aliases = ["@clist", "channels", "comlist", "chanlist", "channellist", "all channels"]
    help_category = "Comms"
    locks = "cmd: not pperm(channel_banned)"

