from ev import default_cmds

class CmdSysRSS2Chan(default_cmds.CmdRSS2Chan):
    """
    @rss2chan - link evennia channel to an RSS feed

    Usage:
      @rss2chan[/switches] <evennia_channel> = <rss_url>

    Switches:
      /disconnect - this will stop the feed and remove the connection to the channel.
      /remove     -                                 "
      /list       - show all rss->evennia mappings

    Example:
      @rss2chan rsschan = http://code.google.com/feeds/p/evennia/updates/basic

    This creates an RSS reader  that connects to a given RSS feed url. Updates will be
    echoed as a title and news link to the given channel. The rate of updating is set
    with the RSS_UPDATE_INTERVAL variable in settings (default is every 10 minutes).

    When disconnecting you need to supply both the channel and url again so as to identify
    the connection uniquely.
    """

    key = "@rss2chan"
    locks = "cmd:serversetting(RSS_ENABLED) and (perm(command_@rss2chan) or perm(Custodians))"
    help_category = "--- Coder/Sysadmin ---"

