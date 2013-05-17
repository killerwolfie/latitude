from ev import Command
from ev import syscmdkeys
from ev import default_cmds

class CmdChannel(default_cmds.MuxCommand):
    """
    This is a special command that the cmdhandler calls
    when it detects that the command given matches
    an existing Channel object key (or alias).
    """

    key = syscmdkeys.CMD_CHANNEL
    locks = "cmd:all()"

    def parse(self):
        channelname, msg = self.args.split(':', 1)
        self.args = channelname.strip(), msg.strip()

    def func(self):
        """
        Create a new message and send it to channel, using
        the already formatted input.
        """
        caller = self.caller
        channelkey, msg = self.args
        if not msg:
            caller.msg("Say what?")
            return
        channel = Channel.objects.get_channel(channelkey)
        if not channel:
            caller.msg("Channel '%s' not found." % channelkey)
            return
        if not channel.has_connection(caller):
            string = "You are not connected to channel '%s'."
            caller.msg(string % channelkey)
            return
        if not channel.access(caller, 'send'):
            string = "You are not permitted to send to channel '%s'."
            caller.msg(string % channelkey)
            return
        msg = "[%s] %s: %s" % (channel.key, caller.name, msg)
        msgobj = create.create_message(caller, msg, channels=[channel])
        channel.msg(msgobj)

