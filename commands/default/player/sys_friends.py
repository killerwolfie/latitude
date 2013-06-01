from ev import default_cmds, utils
from game.gamesrc.latitude.utils.search import match, match_character

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

      @friends/whereis <character>
        Shows you some details on the whereabouts of another character, if
        they're on your friend list.

      @friends add=<player/character>
        Add a player to your friend list.
        You can specify the player or the character name, but either way, the
        player is added to your friend list.
        In order for a friend to appear on your list, you must both add each
        other.

      @friends del=<player/character>
        Remove a player from your friend list.

      @friends optout=[!]<character>
        Specify one of your own characters to opt out of the friend system.
        Opting out a character will make that character invisible to your
        friends.  The system will try its best to conseal the fact that this
        character belongs to you.
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
            online_friends.append('{n%s{n (%s{n)' % (friend_char.return_title(self.caller), friend_char.get_owner().return_title(self.caller)))
        for friend in self.caller.get_friend_players(online_only=True):
            if not friend.get_all_puppets(): # @ooc friend
                online_friends.append('{c%s{n' % (friend.key))
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
                    self.msg('+ ' + friend_char.return_title(self.caller))
                else:
                    # List the characters, unless there is only one character, and it has the same name as the player.
                    friend_chars_online = []
                    friend_chars_offline = []
                    for char in friend_playable_characters:
                        # Don't include characters if they have 'opted out' from the friend system
                        if char.db.friends_optout:
                            continue
                        friend_chars_online.append('{n  - ' + char.return_title(self.caller))
                    friend_chars_online.sort()
                    friend_chars_offline.sort()
                    # Output the resulting entry
                    self.msg('+ ' + friend.return_title(self.caller))
                    if friend_chars_online or friend_chars_offline:
                        self.msg("\n".join(friend_chars_online + friend_chars_offline))
        for character in self.caller.get_playable_characters():
            if character.db.friends_optout:
                self.msg('{ROpt-out: %s' % character.key)
   
    def cmd_add(self, targetname):
        player = self.caller
        target = match(targetname, exact=True)
        if hasattr(target, 'get_owner'):
            target = target.get_owner()
        if not target:
            self.msg('{RPlayer not found.')
            return
        # Check if this player is already a friend
        if target in player.get_friend_players():
            self.msg('"%s" is already your friend.' % target.key)
            return
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
        target = match(targetname, exact=True)
        if hasattr(target, 'get_owner'):
            target = target.get_owner()
        if not target:
            self.msg('{RPlayer not found.')
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
            self.msg('{RPlayer not found.')
            return
        if target.get_owner() != self.caller:
            self.msg('"%s" is not one of your characters.' % (target.key))
            return
        target.db.friends_optout = optout
        if optout:
            self.msg('"%s" is now invisible to the friend system.' % (target.key))
        else:
            self.msg('"%s" has opted back into the friend system.' % (target.key))

    def cmd_whereis(self, targetname):
        friend = match_character(targetname, exact=False)
        if not friend:
            self.msg('{RCharacter not found.')
            return
#        if not friend in self.caller.get_friend_characters(online_only=False):
#            self.msg('{R%s is not on your friend list.' % (friend.key))
#            return
        friend_location = friend.location
        if not friend_location:
            # TODO: Once it's implemented, we'll have to check for 'wandering' here, and report the region as their location.
            self.msg("Your friend doesn't appear to be anywhere in particular.")
        else:
            friend_map = friend.return_map()
            friend_area = friend_location.get_area()
            if friend_area:
                friend_region = friend_area.get_region()
            else:
                friend_region = None
            if friend_map:
                self.msg(friend_map)
            location_tree = []
            for location in [friend_location, friend_area, friend_region]:
                location_name = None
                if hasattr(location, 'objsub_w'):
                    location_name = location.objsub_w()
                elif hasattr(location, 'get_name_within'):
                    location_name = location.get_name_within()
                if location_name:
                    location_tree.append(location_name)
            self.msg("%s is %s." % (friend.key, ", ".join(location_tree)))

    def check_optout(self):
        if not self.caller.status_online():
            self.msg('{RSorry.  All of your currently connected characters are opting out of the friend system.')
            self.msg('{RTo continue using the friend system, you need to connect at least one character without the "opt out" flag, or you can remove it with:')
            self.msg('{r  @friends optout=!<character>')
            return False
        return True
