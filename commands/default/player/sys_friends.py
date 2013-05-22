from ev import default_cmds
from game.gamesrc.latitude.utils.search import match_player, match_character

class CmdSysFriends(default_cmds.MuxPlayerCommand):
    """
    @friends

    Manage your friend list.

    Usage:
      @friends
        Displays a list of your friends who are currently online, and their
        character names.

      @friends/list
        Displays all the friends currently in your list.  Also lists any
        opt-outs you may have in place.

      @friends add=<player/character>
        Add a player to your friend list.
        You can specify the player or the character name, but either way, the
        player is added to your friend list.
        In order for a friend to appear on your list, you must both add each
        other.

      @friends del=<player/character>
        Remove a player from your friend list.

      @friends optout=[!]<player/character>
        Specify one of your own characters (or your player) to opt out of the
        friend system.  Opting out a character will make that character
        invisible to your friends, but that character will also be unable to
        use the friend list or any benefits of the friend system, and friend
        requests using that character name will be automatically rejected.
        Opting out your player causes the same effect for all your characters,
        and all friend requests will be automatically rejected.  Use ! to
        remove the opt-out flag from one of your characters or your player.

    """

    key = "@friends"
    locks = "cmd:all()"
    aliases = ['wf']
    help_category = "General"

    def func(self):
        if not self.switches and not self.args:
            self.cmd_online()
            return
        elif self.switches == [ 'list' ] and not self.args:
            self.cmd_list()
            return
        elif not self.switches and self.lhs == 'add' and self.rhs:
            self.cmd_add(self.rhs)
            return
        elif not self.switches and self.lhs == 'del' and self.rhs:
            self.cmd_del(self.rhs)
            return
        elif not self.switches and self.lhs == 'optout' and self.rhs:
            self.cmd_optout(self.rhs)
            return
        # Unrecognized command
        self.msg("Invalid '%s' command.  See 'help %s' for usage" % (self.cmdstring, self.key))

    def cmd_online(self):
        if not self.check_optout():
            return
        online_friends = []
        for friend_char in sorted(self.caller.get_friend_characters(online_only=True), key=lambda char: char.key.lower()):
            online_friends.append('{c%s{n ({c%s{n)' % (friend_char.key, friend_char.db.owner))
        if online_friends:
            self.msg('Online friends: ' + "{n, ".join(online_friends))
        else:
            self.msg('None of your friends are currently online.')

    def cmd_list(self):
        if not self.check_optout():
            return
        friends = self.caller.get_friend_players()
        if not friends:
            self.msg('You have no friends :(')
        else:
            for friend in sorted(friends, key=lambda friend_player: str(friend_player).lower()):
                friend_playable_characters = friend.get_playable_characters()
                if not friend_playable_characters:
                    continue
                if len(friend_playable_characters) == 1 and friend_playable_characters[0].key.lower() == friend.key.lower():
                    # If this player only has one character and it matches the name of the player exactly, then output a condensed entry
                    friend_char = friend_playable_characters[0]
                    if friend_char.db.friends_optout:
                        continue
                    self.msg('+ ' + (friend_char.sessid and '{c' or '{C') + friend_char.key)
                else:
                    # List the characters, unless there is only one character, and it has the same name as the player.
                    friend_chars_online = []
                    friend_chars_offline = []
                    for char in friend_playable_characters:
                        # Don't include characters if they have 'opted out' from the friend system
                        if char.db.friends_optout:
                            continue
                        if char.sessid:
                            friend_chars_online.append('{n  - {c' + char.key)
                        else:
                            friend_chars_offline.append('{n  - {C' + char.key)
                    friend_chars_online.sort()
                    friend_chars_offline.sort()
                    # Output the resulting entry
                    self.msg('+ ' + (friend_chars_online and '{c' or '{C') + friend.key)
                    if friend_chars_online or friend_chars_offline:
                        self.msg("\n".join(friend_chars_online + friend_chars_offline))
        for character in self.caller.get_playable_characters():
            if character.db.friends_optout:
                self.msg('{ROpt-out: %s' % character.key)
   
    def cmd_add(self, targetname):
        player = self.caller
        target = match_player(targetname, exact=True)
        if not target:
            self.msg('Player not found.')
            return
        # Check if this player is already a friend
        if target in player.get_friend_players():
            self.msg('%s is already your friend.' % target.key)
        # Add the player to the friend list if needed
        if player in target.db.friends_list:
            # Already in the target's friend list.  Mutual friendship begins!  Bunnies and rainbows.
            player.db.friends_list.add(target)
            self.msg('Added "%s" as a friend!' % target.key)
        else:
            # Alert the target user (only if this isn't already a 'friend request' state.)
            if not target in player.db.friends_list:
                self.msg('STUB: Alert other user.  Mail system?')
            player.db.friends_list.add(target)
            # Not already in the target's friend list, so let them know this is only a 'friend request' state.
            self.msg('Friend request sent.  In order for this player to appear in your friend list, they will have to add you as well.  Use %s/del %s to cancel the request if needed.' % (self.key, targetname))

    def cmd_del(self, targetname):
        player = self.caller
        target = match_player(targetname, exact=True)
        if not target:
            self.msg('Player not found.')
            return
        if target in player.get_friend_players():
            if target in player.db.friends_list:
                player.db.friends_list.remove(target)
            if player in target.db.friends_list:
                target.db.friends_list.remove(player)
            self.msg("You're no longer friends with \"%s\" D:", target.key)
        else:
            if target in player.db.friends_list:
                player.db.friends_list.remove(target)
            self.msg('Cancelling any outstanding friend requests with "%s".', targetname)

    def cmd_optout(self, targetname):
        if targetname[:1] == '!':
            optout = False
            target = match_character(targetname[1:], exact=True)
        else:
            optout = True
            target = match_character(targetname, exact=True)
        if not target:
            self.msg('Player not found.')
            return
        if target.get_owner() != self.caller:
            self.msg('"%s" is not one of your characters.' % (target.key))
            return
        target.db.friends_optout = optout
        if optout:
            self.msg('"%s" is now invisible to the friend system.' % (target.key))
        else:
            self.msg('"%s" has opted back into the friend system.' % (target.key))

    def check_optout(self):
        optout_characters = set([str(char) for char in self.caller.get_all_puppets() if char.db.friends_optout])
        if optout_characters:
            self.msg('{RSorry.  One or more of your currently connected characters are opting out of the friend system.  ({r%s{R)' % ", ".join(optout_characters))
            self.msg('{RTo continue using the friend system, either disconnect those characters, or remove the "opt out" flag with:')
            self.msg('{r  @friends optout=!<character>')
            return False
        return True
