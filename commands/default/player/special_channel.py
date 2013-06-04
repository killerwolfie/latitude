from ev import syscmdkeys, Channel, create_message
from game.gamesrc.latitude.commands.default.character import say

class CmdChannel(say.CmdSay):
    """
    This is a special command that the cmdhandler calls
    when it detects that the command given matches
    an existing Channel object key (or alias).
    """

    key = syscmdkeys.CMD_CHANNEL
    aliases = []
    locks = "cmd:all()"

    def parse(self):
        super(CmdChannel, self).parse()
        channelname, msg = self.args.split(':', 1)
        self.args = channelname.strip(), msg.strip()

    def func(self):
        """
        Create a new message and send it to the channel
        """
        player = self.caller
        # Check arguments
        channelkey, message = self.args
        if not message:
            self.msg("{RSay what?")
            return
        channel = Channel.objects.get_channel(channelkey)
        if not channel:
            self.msg("{RChannel '%s' not found." % channelkey)
            return
        # Verify permissions
        if not channel.has_connection(player):
            self.msg("{RYou are not connected to channel '%s'." % channelkey)
            return
        if not channel.access(player, 'send'):
            self.msg("{RYou are not permitted to send to channel '%s'." % channelkey)
            return
        # Format the message
        if self.character:
            # If we have a character, then we can use the 'say' routines to format the message.
            if message.startswith(':'):
                message = self.gen_pose(message[1:])
            elif message.startswith('"'):
                message = self.gen_say(message[1:])
            else:
                message = self.gen_say(message)
        else:
            # If we have no character, we'll have to take care of the formatting
            if message.startswith(':'):
                message = '{b' + player.key + '{n ' + message[1:].replace('{', '{{').replace('%', '%%')
            elif message.startswith('"'):
                message = '{b' + player.key + '{n: ' + message[1:].replace('{', '{{').replace('%', '%%')
            else:
                message = '{b' + player.key + '{n: ' + message.replace('{', '{{').replace('%', '%%')
        message = "[%s] " % (channel.key) + message
        # Send it
        msgobj = create_message(player, message, channels=[channel])
        channel.msg(msgobj)

