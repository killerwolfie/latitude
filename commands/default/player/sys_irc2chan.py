from ev import default_cmds

class CmdSysIRC2Chan(default_cmds.CmdIRC2Chan):
    """
    @irc2chan - link evennia channel to an IRC channel

    Usage:
      @irc2chan[/switches] <evennia_channel> = <ircnetwork> <port> <#irchannel> <botname>

    Switches:
      /disconnect - this will delete the bot and remove the irc connection to the channel.
      /remove     -                                 "
      /list       - show all irc<->evennia mappings

    Example:
      @irc2chan myircchan = irc.dalnet.net 6667 myevennia-channel evennia-bot

    This creates an IRC bot that connects to a given IRC network and channel. It will
    relay everything said in the evennia channel to the IRC channel and vice versa. The
    bot will automatically connect at server start, so this comman need only be given once.
    The /disconnect switch will permanently delete the bot. To only temporarily deactivate it,
    use the @services command instead.
    """

    key = "@irc2chan"
    locks = "cmd:perm(command_@irc2chan) or perm(Janitors)"
    help_category = "=== Admin ==="

