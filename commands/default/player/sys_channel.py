from ev import default_cmds, utils
from src.utils import prettytable
from src.comms.models import Channel, PlayerChannelConnection

class CmdSysChannel(default_cmds.MuxPlayerCommand):
    """
    @channel - manage your channel subscriptions

    Usage:
       @channel
       @channel/list
         Outputs a list of available channels.

       @channel/who
       @channel/who <channel>
         Displays everyone who's currently listening to a channel.  By default it
         displays all channels you're currently subscribed to.

       @channel/sub <channel>
         Subscribes to a channel.

       @channel/unsub <channel>
         Unsubscribes from a channel.
    """

    key = "@channel"
    aliases = []
    help_category = "Communication"
    locks = "cmd:all()"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        switches = [switch.lower() for switch in self.switches]
        if (not self.switches or self.switches == [ 'list' ]) and not self.args:
            self.cmd_list()
        elif self.switches == [ 'who' ]:
            self.cmd_who(self.args)
        elif self.switches == [ 'sub' ] and self.args:
            self.cmd_sub(self.args)
        elif self.switches == [ 'unsub' ] and self.args:
            self.cmd_unsub(self.args)
        else:
            # Unrecognized command
            self.msg("Invalid '%s' command.  See 'help %s' for usage" % (self.cmdstring, self.key))
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")

    def cmd_list(self):
        caller = self.caller
        # Get all channels we have available to listen to
        channels = [chan for chan in Channel.objects.get_all_channels() if chan.access(caller, 'listen')]
        if not channels:
            self.msg("No channels available.")
            return
        # Get all channel we are already subscribed to
        subs = [conn.channel for conn in PlayerChannelConnection.objects.get_all_player_connections(caller)]
        # Show the user a table
        comtable = prettytable.PrettyTable(["{CSub", "{CChannel", "{CDescription"], border=False)
        comtable.add_row(['', '', ''])
        for chan in channels:
            nicks = [nick for nick in caller.nicks.get(nick_type="channel")]
            comtable.add_row([chan in subs and "{GYes{n" or "{RNo{n", "%s%s" % (chan.key, chan.aliases and " (%s)" % ",".join(chan.aliases) or ""), chan.desc])
        self.msg(comtable)

    def cmd_who(self, channelname):
        caller = self.caller
        # Find the requested channel(s)
        if channelname:
            channels = Channel.objects.channel_search(channelname) or [chan for chan in Channel.objects.all() if channelname in chan.aliases]
            if not channels:
                self.msg('Channel "%s" not found.' % (channelname))
                return
            if len(channels) > 1:
                self.msg('Multiple channels match (be more specific):\n%s' % (', '.join([["%s(%s)" % (chan.key, chan.id) for chan in channels]])))
                return
        else:
            channels = [conn.channel for conn in PlayerChannelConnection.objects.get_all_player_connections(caller)]
        # Check permissions
        for channel in channels:
            if not channel.access(self.caller, "listen"):
                self.msg("You can't access this channel.")
                return
            self.msg('{C%s:' % channel.key)
            players = [conn.player for conn in PlayerChannelConnection.objects.get_all_connections(channel) if conn.player.status_online()]
            if players:
                self.msg('  ' + ', '.join([player.get_desc_styled_name(caller) for player in players]))
            else:
                self.msg('  <None>')

    def cmd_sub(self, channelname):
        player = self.caller
        # Find the requested channel
        channels = Channel.objects.channel_search(channelname) or [chan for chan in Channel.objects.all() if channelname in chan.aliases]
        if not channels:
            self.msg('Channel "%s" not found.' % (channelname))
            return
        if len(channels) > 1:
            self.msg('Multiple channels match (be more specific):\n%s' % (', '.join([["%s(%s)" % (chan.key, chan.id) for chan in channels]])))
            return
        channel = channels[0]
        # Check permissions
        if not channel.access(player, 'listen'):
            self.msg("%s: You are not allowed to listen to this channel." % channel.key)
            return
        if channel.has_connection(player):
            self.msg("You are already connected to channel %s." % channel.key)
            return
        # Connect to the channel
        if channel.connect_to(player):
            self.msg("You now listen to the channel %s. " % channel.key)
        else:
            self.msg("%s: You are not allowed to join this channel." % channel.key)

    def cmd_unsub(self, channelname):
        player = self.caller
        # Find the requested channel
        channels = Channel.objects.channel_search(channelname) or [chan for chan in Channel.objects.all() if channelname in chan.aliases]
        if not channels:
            self.msg('Channel "%s" not found.' % (channelname))
            return
        if len(channels) > 1:
            self.msg('Multiple channels match (be more specific):\n%s' % (', '.join([["%s(%s)" % (chan.key, chan.id) for chan in channels]])))
            return
        channel = channels[0]
        # Unsubscribe from the channel
        if channel.has_connection(player):
            channel.disconnect_from(player)
            self.msg("You stop listening to channel '%s'." % channel.key)
        else:
            self.msg("You are not listening to that channel.")
