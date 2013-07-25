from ev import utils, create_message
from game.gamesrc.latitude.utils.search import match, match_character
import pickle
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysFriends(LatitudeCommand):
    """
    @friends - Manage your friend list.

    Usage:
      @friends
        Displays a list of your friends who are currently online, and their
        character names.

      @friends/list
        Displays all the friends currently in your list.  Also lists any
        opt-outs you may have in place.

      @friends/whereis <character>
        Shows you some details on the whereabouts of another character, if they're
        on your friend list.

      @friends/add <player/character>
        Add a player to your friend list.
        You can specify the player or the character name, but either way, the
        player is added to your friend list.
        In order for a friend to appear on your list, you must both add each
        other.

      @friends/del <player/character>
        Remove a player from your friend list.

      @friends/optout [!]<character>
        Specify one of your own characters to opt out of the friend system.
        Opting out a character will make that character invisible to your friends.
        The system will try its best to conceal the fact that this character
        belongs to you.
        Use ! to remove the opt-out flag from one of your characters.
    """

    key = "@friends"
    locks = "cmd:all()"
    aliases = ['wf', '@whereis', 'whereis']
    help_category = "General"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        if self.cmdstring.lower() == '@whereis' or self.cmdstring.lower() == 'whereis':
            if not self.switches and self.args:
                self.cmd_whereis(self.args)
                return
        else:
            if not self.switches and not self.args:
                self.cmd_online()
                return
            elif self.switches == [ 'list' ] and not self.args:
                self.cmd_list()
                return
            elif self.switches == [ 'whereis' ] and self.args:
                self.cmd_whereis(self.args)
                return
            elif self.switches == [ 'add' ] and self.args:
                self.cmd_add(self.args)
                return
            elif self.switches == [ 'del' ] and self.args:
                self.cmd_del(self.args)
                return
            elif self.switches == [ 'optout' ] and self.args:
                self.cmd_optout(self.args)
                return
        # Unrecognized command
        self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))

    def cmd_online(self):
        if not self.check_optout():
            return
        online_friends = []
        for friend_char in sorted(self.player.get_friend_characters(online_only=True), key=lambda char: char.key.lower()):
            online_friends.append('{Y%s{Y (%s{Y)' % (friend_char.get_desc_styled_name(self.player), friend_char.get_owner().get_desc_styled_name(self.player)))
        for friend in self.player.get_friend_players(online_only=True):
            if not friend.get_all_puppets(): # @ooc friend
                online_friends.append('{c%s{n' % (friend.key))
        if online_friends:
            self.msg('{Y[Online friends: ' + "{Y, ".join(online_friends) + '{Y]')
        else:
            self.msg('{Y[None of your friends are currently online.]')

    def cmd_list(self):
        if not self.check_optout():
            return
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        friends = self.player.get_friend_players()
        if not friends:
            self.msg('You have no friends :(')
        else:
            for friend in sorted(friends, key=lambda friend_player: str(friend_player).lower()):
                friend_characters = friend.get_characters()
                if not friend_characters:
                    continue
                if len(friend_characters) == 1 and list(friend_characters)[0].key.lower() == friend.key.lower():
                    # If this player only has one character and it matches the name of the player exactly, then output a condensed entry
                    friend_char = list(friend_characters)[0]
                    if friend_char.db.friends_optout:
                        continue
                    self.msg('+ ' + friend_char.get_desc_styled_name(self.player))
                else:
                    # List the characters, unless there is only one character, and it has the same name as the player.
                    friend_chars_online = []
                    friend_chars_offline = []
                    for char in friend_characters:
                        # Don't include characters if they have 'opted out' from the friend system
                        if char.db.friends_optout:
                            continue
                        friend_chars_online.append('{n  - ' + char.get_desc_styled_name(self.player))
                    friend_chars_online.sort()
                    friend_chars_offline.sort()
                    # Output the resulting entry
                    self.msg('+ ' + friend.get_desc_styled_name(self.player))
                    if friend_chars_online or friend_chars_offline:
                        self.msg("\n".join(friend_chars_online + friend_chars_offline))
        for character in self.player.get_characters():
            if character.db.friends_optout:
                self.msg('{ROpt-out: %s' % character.key)
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
   
    def cmd_add(self, targetname):
        player = self.player
        target = match(targetname, exact=True)
        if hasattr(target, 'get_owner'):
            target = target.get_owner()
        if not target:
            self.msg('{R[Player not found]')
            return
        # Check if this player is already a friend
        if target in player.get_friend_players():
            self.msg('{R["%s" is already your friend]' % target.key)
            return
        # Ensure they're not trying to befriend themselves
        if target == player:
            self.msg('{G[You befriend yourself {m<3 <3 <3{G]')
            return
        # Add the player to the friend list if needed
        if player in target.db.friends_list:
            # Already in the target's friend list.  Mutual friendship begins!  Bunnies and rainbows.
            player.db.friends_list.add(target)
            self.msg('{G[Added "%s" as a friend!]' % target.key)
            target.msg('{G["%s" added you as a friend!]' % player.key)
        else:
            # Alert the target user
            # Construct message header
            sender = None
            # Get the recipients
            receivers = [target]
            # Collect the message from the user
            message = "{Y[You've received a friend request from %s.  To accept the request, use {y%s/add %s{Y]" % (player.key, self.key, player.key)
            # Generate message header, to store the 'to' and 'from' as provided.  (The recievers and sender field of the Msg object will be the player, and never a character)
            header = {
                'from' : 'Latitude MUD',
                'to' : [target.key],
            }
            header = pickle.dumps(header)
            # Create the message object
            msg_object = create_message(sender, message, receivers=receivers, header=header)
            # Display the message to the user, or mark it as unseen if they're offline so it can be read later
            for receiver in receivers:
                if receiver.sessions:
                    receiver.msg(message)
                else:
                    if not receiver.db.msg_unseen:
                        receiver.db.msg_unseen = []
                    receiver.db.msg_unseen.append(msg_object)
            # Actually add the friend to this player's list
            player.db.friends_list.add(target)
            # Not already in the target's friend list, so let them know this is only a 'friend request' state.
            self.msg('{Y[Friend request sent.  In order for this player to appear in your friend list, they will have to add you as well.  Use {y%s/del %s{Y to cancel the request if needed.]' % (self.key, targetname))

    def cmd_del(self, targetname):
        player = self.player
        target = match(targetname, exact=True)
        if hasattr(target, 'get_owner'):
            target = target.get_owner()
        if not target:
            self.msg('{R[Player not found.]')
            return
        if target in player.get_friend_players():
            if target in player.db.friends_list:
                player.db.friends_list.remove(target)
            if player in target.db.friends_list:
                target.db.friends_list.remove(player)
            self.msg("{G[You're no longer friends with \"%s\"  D:  Sadface.]" % target.key)
        else:
            if target in player.db.friends_list:
                player.db.friends_list.remove(target)
            self.msg('{G[Cancelling any outstanding friend requests with "%s".]' % targetname)

    def cmd_optout(self, targetname):
        if targetname[:1] == '!':
            optout = False
            target = match_character(targetname[1:], exact=True)
        else:
            optout = True
            target = match_character(targetname, exact=True)
        if not target:
            self.msg('{R[Player not found]')
            return
        if target.get_owner() != self.player:
            self.msg('{R["%s" is not one of your characters]' % (target.key))
            return
        target.db.friends_optout = optout
        if optout:
            self.msg('{G["%s" is now invisible to the friend system.]' % (target.key))
        else:
            self.msg('{G["%s" has opted back into the friend system.]' % (target.key))

    def cmd_whereis(self, targetname):
        friend = match_character(targetname, exact=False)
        if not friend:
            self.msg('{R[Character not found]')
            return
#        if not friend in self.player.get_friend_characters(online_only=False):
#            self.msg('{R%s is not on your friend list.' % (friend.key))
#            return
        friend_location = friend.location
        if not friend_location:
            self.msg("Your friend doesn't appear to be anywhere in particular.")
        else:
            friend_map = friend.get_desc_map()
            if friend_map:
                self.msg(friend_map)
            self.msg('%s is %s.' % (friend.key, ", ".join([inside.objsub('&0w') for inside in friend_location.trace()])))

    def check_optout(self):
        if not self.player.status_online():
            self.msg('{R[Sorry.  All of your currently connected characters are opting out of the friend system.]')
            self.msg('{R[To continue using the friend system, you need to connect at least one character without the "opt out" flag, or you can remove it with: {r@friends optout=!<character>{R]')
            return False
        return True
