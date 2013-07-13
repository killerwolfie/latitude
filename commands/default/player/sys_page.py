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
    aliases = ['p', 'page']
    locks = "cmd:all()"
    help_category = "Communication"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        self.switches = [switch.lower() for switch in self.switches]
        if (not self.switches or self.switches == ['last']) and not self.args:
            self.cmd_last()
            return
        elif (not self.switches or self.switches == ['last']) and self.args.isdigit():
            self.cmd_last(num=int(self.args))
        elif not self.switches and self.rhs:
            self.cmd_page(targetstr=self.lhs, message=self.rhs, mail=False)
        elif self.switches == ['mail'] and self.rhs:
            self.cmd_page(targetstr=self.lhs, message=self.rhs, mail=True)
        else:
            # Unrecognized command
            self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))

    def cmd_last(self, num=None):
        player = self.caller
        if num:
            # Make sure the user didn't put in something silly
            if num > 10:
                self.msg('{R[Sorry, you can only display a maximum of 10 messages]')
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
                self.msg('{Y[You have no page history]')
                return
        else:
            if player.db.msg_unseen:
                lastpages = player.db.msg_unseen
                player.db.msg_unseen = None
            else:
                self.msg('{Y[You have no unread pages.]')
                return
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        output = []
        for page in lastpages:
            if page.header:
                header = pickle.loads(page.header)
                output.append("{n---- {nMessage from {C%s{n to {C%s{n at %s{n ----\n{n%s" % (header['from'], conj_join(['{C' + tostr + '{n' for tostr in header['to']], 'and'), utils.datetime_format(page.date_sent), page.message))
            else:
                output.append("{n---- {nMessage sent at %s{n ----\n{n%s" % (utils.datetime_format(page.date_sent), page.message))
        self.msg("\n\n".join(output))
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")

    def cmd_page(self, targetstr, message, mail=False):
        player = self.caller
        sender = player.get_puppet(self.sessid) or player
        # Identify the recipients
        if not targetstr:
            # Grab the last page that we sent to
            lastpages = Msg.objects.get_messages_by_sender(player, exclude_channel_messages=True)
            if not lastpages:
                self.msg('{R[Could not re-send to previous recipient: No pages sent]')
            lastpages.sort(cmp=lambda x, y: cmp(x.date_sent, y.date_sent))
            # Extract the header
            header = lastpages[-1].header
            if not header:
                self.msg("{R[Could not re-send to previous recipient: Your last page didn't have any sender information]")
                return
            header = pickle.loads(header)
            if not 'from' in header or not 'to' in header:
                self.msg("{R[Could not re-send to previous recipient: Your last page didn't have any sender/recipients]")
                return
            new_targets = set(header['to'])
            targetstr = ','.join(new_targets)
        elif targetstr.lower() == '#r':
            # Grab the last received page
            lastpages = Msg.objects.get_messages_by_receiver(player)
            if not lastpages:
                self.msg('{R[Could not reply: No pages received]')
            lastpages.sort(cmp=lambda x, y: cmp(x.date_sent, y.date_sent))
            # Extract the header
            header = lastpages[-1].header
            if not header:
                self.msg("{R[Could not reply: Your last page didn't have any sender information]")
                return
            header = pickle.loads(header)
            if not 'from' in header or not 'to' in header:
                self.msg("{R[Could not reply: Your last page didn't have any sender/recipients]")
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
            targetname = targetname.strip()
            receiver = match(targetname, prioritize_players=True)
            if receiver:
                receivers.add(receiver)
            else:
                self.msg('{R[Could not find "%s", cancelling message]' % (targetname))
                return
        # Verify that everyone is online
        if not mail:
            for receiver in receivers:
                if not receiver.status_online():
                    self.msg('{R["%s" is not currently online, cancelling message]' % (receiver.key))
                    self.msg("{R[If you want to send a message to someone who's offline, use '{r%s/mail{R', and they will be alerted the next time they log in]" % (self.key))
                    self.msg("{R[See {rhelp %s{R for details]" % (self.key))
                    return
        # Generate message header, to store the 'to' and 'from' as provided.  (The recievers and sender field of the Msg object will be the player, and never a character)
        header = {
            'from' : sender.key,
            'to' : [obj.key for obj in receivers],
        }
        header = pickle.dumps(header)
        # Construct the message text itself.  Must be called before the sender and receiver are converted into players.
        message = self.gen_message_text(sender, receivers, message)
        # Create the persistent message object
        receiver_players = set()
        for receiver in receivers:
            if utils.inherits_from(receiver, "src.objects.objects.Character"):
                receiver_players.add(receiver.get_owner())
            else:
                receiver_players.add(receiver)
        msg_object = create_message(player, message, receivers=receiver_players, header=header)
        # If this is a 'mail' then deliver the message into their 'unseen' list.
        if mail:
            for receiver_player in receiver_players:
                if not receiver_player.db.msg_unseen:
                    receiver_player.db.msg_unseen = []
                receiver_player.db.msg_unseen.append(msg_object)
        # Tell the players they got a message.
        if mail:
            for receiver_player in receiver_players:
                receiver_player.msg("{Y[You've received a page mail.  Use \"{y@page{Y\" to view it]")
            if player not in receiver_players:
                self.msg('{G[Page mail sent]')
        else:
            # To eliminate duplicates, produce a set() of sessid/player pairs.
            msg_targets = set()
            msg_targets.add((player, self.sessid))
            for receiver in receivers:
                if utils.inherits_from(receiver, "src.objects.objects.Character"):
                    msg_targets.add((receiver.player, receiver.sessid))
                else: # Player
                    for session in receiver.get_all_sessions():
                        msg_targets.add((receiver, session.sessid))
            for msg_target in msg_targets:
                msg_target[0].msg('{Y[Page] {n' + message, sessid=msg_target[1])

    def gen_message_text(self, sender, receivers, raw_message):
        """
        Produces a pretty version of the message string requested by the user, handling page poses, etc.
        """
        character = self.character
        player = self.caller
        message = raw_message
        if character:
            # If we have a character, then we can use the 'say' routines to format the message.
            if message.startswith(':'):
                message = character.speech_pose(message[1:])
            elif message.startswith('"'):
                message = character.speech_say(message[1:])
            else:
                message = character.speech_say(message)
        else:
            # If we have no character, we'll have to take care of the formatting
            if message.startswith(':'):
                message = '{b' + player.key + '{n ' + message[1:].replace('{', '{{').replace('%', '%%')
            elif message.startswith('"'):
                message = '{b' + player.key + '{n: ' + message[1:].replace('{', '{{').replace('%', '%%')
            else:
                message = '{b' + player.key + '{n: ' + message.replace('{', '{{').replace('%', '%%')
        if len(receivers) > 1:
            message = "{Y(To %s) {n%s" % (conj_join([obj.key for obj in receivers], 'and'), message)
        return message
