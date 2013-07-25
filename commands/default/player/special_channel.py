from ev import syscmdkeys, Channel, create_message
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdChannel(LatitudeCommand):
    key = syscmdkeys.CMD_CHANNEL
    aliases = []
    locks = "cmd:all()"
    auto_help = False

    def parse(self):
        super(CmdChannel, self).parse()
        channelname, msg = self.args.split(':', 1)
        self.args = channelname.strip(), msg.strip()

    def func(self):
        """
        Create a new message and send it to the channel
        """
        player = self.player
        # Check arguments
        channelkey, message = self.args
        if not message:
            self.msg("{R[Say what?]")
            return
        channel = Channel.objects.get_channel(channelkey)
        if not channel:
            self.msg("{R[Channel '%s' not found]" % channelkey)
            return
        # Verify permissions
        if not channel.has_connection(player):
            self.msg("{R[You are not connected to channel '%s']" % channelkey)
            return
        if not channel.access(player, 'send'):
            self.msg("{R[You are not permitted to send to channel '%s']" % channelkey)
            return
        # Format the message
        if self.character:
            # If we have a character, then we can use the 'say' routines to format the message.
            if message.startswith(':'):
                message = self.character.speech_pose(message[1:])
            elif message.startswith('"'):
                message = self.character.speech_say(message[1:])
            else:
                message = self.character.speech_say(message)
        else:
            # If we have no character, we'll have to take care of the formatting
            if message.startswith(':'):
                message = '{b' + player.key + '{n ' + message[1:].replace('{', '{{').replace('%', '%%')
            elif message.startswith('"'):
                message = '{b' + player.key + '{n: ' + message[1:].replace('{', '{{').replace('%', '%%')
            else:
                message = '{b' + player.key + '{n: ' + message.replace('{', '{{').replace('%', '%%')
        message = "{Y[ {g%s {Y| {n%s {Y]" % (channel.key, message)
        # Send it
        msgobj = create_message(player, message, channels=[channel])
        channel.msg(msgobj)

