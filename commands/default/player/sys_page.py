from ev import default_cmds, create_message, utils
from src.comms.models import Msg
from game.gamesrc.latitude.utils.search import match, match_character
from game.gamesrc.latitude.utils.stringmanip import conj_join
import pickle

class CmdSysPage(default_cmds.MuxPlayerCommand):
    """
    @page - Send a private message

    Usage:
      @page <player/character>[,<player/character>,...]=<message/:pose>
      @page #r=<message/:pose>
      @page #R=<message/:pose>
        Send a message to one or more players.

      @page/mail <player/character>[,<player/character>,...]=<message/:pose>
        Send a message to one or more players, even if some or all of them are offline.

      @page/last [<number>] (default)
        View your last <number> pages.  By default, it shows pages which have not yet been seen.
    """

    key = "@page"
    aliases = ['page']
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        self.switches = [switch.lower() for switch in self.switches]
        if (not self.switches or self.switches == ['last']) and not self.args:
            self.cmd_last()
            return
        elif (not self.switches or self.switches == ['last']) and self.args.isdigit():
            self.cmd_last(num=int(self.args))
        elif not self.switches and self.lhs and self.rhs:
            self.cmd_page(targetstr=self.lhs, message=self.rhs, mail_offline=False)
        elif self.switches == ['mail'] and self.lhs and self.rhs:
            self.cmd_page(targetstr=self.lhs, message=self.rhs, mail_offline=True)
        else:
            # Unrecognized command
            self.msg("Invalid '%s' command.  See 'help %s' for usage." % (self.cmdstring, self.key))

    def cmd_last(self, num=None):
        player = self.caller
        if num:
            # Make sure the user didn't put in something silly
            if num > 10:
                self.msg('{RSorry, you can only display a maximum of 10 messages.')
                return
            # Get the messages we've sent (not to channels)
            pages = set(Msg.objects.get_messages_by_sender(player, exclude_channel_messages=True))
            # Get the messages we've received
            pages |= set(Msg.objects.get_messages_by_receiver(player))
            # Sort them in chronological order
            pages = sorted(pages, cmp=lambda x, y: cmp(x.date_sent, y.date_sent))
            # Grab only the last 'num' pages
            if len(pages) > num:
                lastpages = pages[-num:]
            else:
                lastpages = pages
            if not lastpages:
                self.msg('You have no page history.')
                return
        else:
            if player.db.msg_unseen:
                lastpages = player.db.msg_unseen
                player.db.msg_unseen = None
            else:
                self.msg('You have no unread pages.')
                return
        self.msg('Your latest %spages:' % (num and '' or '(offline) '))
        output = []
        for page in lastpages:
            if page.header:
                header = pickle.loads(page.header)
                output.append("{n---- {nMessage from {C%s{n to {C%s{n at %s{n ----\n{n%s" % (header['from'], conj_join(['{C' + tostr + '{n' for tostr in header['to']], 'and'), utils.datetime_format(page.date_sent), page.message))
            else:
                output.append("{n---- {nMessage sent at %s{n ----\n{n%s" % (utils.datetime_format(page.date_sent), page.message))
        self.msg("\n\n".join(output))

    def cmd_page(self, targetstr, message, mail_offline=False):
        player = self.caller
        sender = player.get_puppet(self.sessid) or player
        # Identify the recipients
        if targetstr.lower() == '#r':
            # Grab the last received page
            lastpages = Msg.objects.get_messages_by_receiver(player)
            if not lastpages:
                self.msg('{RCould not reply: No pages received.')
            lastpages.sort(cmp=lambda x, y: cmp(x.date_sent, y.date_sent))
            # Extract the header
            header = lastpages[-1].header
            if not header:
                self.msg("{RCould not reply: Your last page didn't have any sender information.")
                return
            header = pickle.loads(header)
            if not 'from' in header or not 'to' in header:
                self.msg("{RCould not reply: Your last page didn't have any sender/recipients.")
                return
            new_targets = set()
            if targetstr == '#R':
                # Append the recipients of the previous messages, then strip out yourself, if applicable.
                new_targets |= set(header['to'])
                if sender.key in new_targets:
                    new_targets.remove(sender.key)
            # Append the sender of the previous message, whether it's yourself or not.
            new_targets |= set([header['from']])
            targetstr = ','.join(new_targets)
        # Convert the requested names into character/player objects
        receivers = set()
        for targetname in targetstr.split(','):
            receiver = match(targetname)
            if receiver:
                receivers.add(receiver)
            else:
                self.msg('{RCould not find "%s", cancelling message.' % (targetname))
                return
        # Verify that everyone is online
        if not mail_offline:
            for receiver in receivers:
                if not receiver.shows_online():
                    self.msg('{R"%s" is not currently online.  Cancelling message.' % (receiver.key))
                    self.msg("{RIf you want to send a message to someone who's offline, use '%s/mail', and they will be alerted the next time they log in." % (self.key))
                    self.msg("{RSee help %s for details" % (self.key))
                    return
        # Generate message header, to store the 'to' and 'from' before they get converted into player objects
        header = {
            'from' : sender.key,
            'to' : [obj.key for obj in receivers],
        }
        header = pickle.dumps(header)
        # Construct the message text itself.  Must be called before the sender and receiver are converted into players.
        message = self.gen_message_text(sender, receivers, message)
        # Convert the sender and receivers into player objects
        if hasattr(sender, 'get_owner'):
            sender = sender.get_owner()
        receivers = list(set([obj.get_owner() for obj in receivers if hasattr(obj, 'get_owner')]))
        # Create the persistent message object
        msg_object = create_message(player, message, receivers=receivers, header=header)
        # Tell the players they got a message.
        for receiver in receivers:
            if receiver.sessions:
                # Player is olnise
                receiver.msg(message)
            else:
                # Player is offline
                if not receiver.db.msg_unseen:
                    receiver.db.msg_unseen = []
                receiver.db.msg_unseen.append(msg_object)
        if not sender in receivers:
            sender.msg(message)

    def gen_message_text(self, sender, receivers, raw_message):
        """
        Produces a pretty version of the message string requested by the user, handling page poses, etc.
        """
        message = raw_message
        # Create a page pose if it startes with a :
        if message.startswith(":"):
            message = "%s %s" % (player.key, message.strip(':').strip())
        message = '%s pages, "%s" to %s.' % (sender.key, message, conj_join([obj.key for obj in receivers], 'and'))
        return message
