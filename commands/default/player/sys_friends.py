from ev import default_cmds
from src.utils import prettytable

class CmdSysFriends(default_cmds.MuxCommand):
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
        Add a player to your friend list.  (You can specify the player or the
        character name, but either way, the player is added to your friend
        list)

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
        player = self.caller.player

        online_friends = []
        if player.db.friends_list:
            for friend in sorted(player.db.friends_list, key=lambda friend_player: str(friend_player).lower()):
                if friend.db._playable_characters:
                    for friend_char in friend.db._playable_characters:
                        # Skip characters if they have 'opted out' from the friend system
                        if friend_char.db.friends_optout:
                            continue
                        if friend_char.sessid:
                            online_friends.append('{c%s{n ({c%s{n)' % (friend_char.key, friend.key))
        if online_friends:
            self.msg('Online friends: ' + "{n, ".join(online_friends))
        else:
            self.msg('None of your friends are currently online.')

    def cmd_list(self):
        player = self.caller.player

        if not player.db.friends_list:
            self.msg('You have no friends :(')
        else:
            for friend in sorted(player.db.friends_list, key=lambda friend_player: str(friend_player).lower()):
                self.msg('+ ' + (friend.sessions and '{c' or '{C') + friend.key)
                # Produce a list of this friend's characters
                if friend.db._playable_characters:
                    friend_chars_online = []
                    friend_chars_offline = []
                    for char in friend.db._playable_characters:
                        # Don't include characters if they have 'opted out' from the friend system
                        if char.db.friends_optout:
                            continue
                        if char.sessid:
                            friend_chars_online.append('{n  - {c' + char.key)
                        else:
                            friend_chars_offline.append('{n  - {C' + char.key)
                    friend_chars_online.sort()
                    friend_chars_offline.sort()
                    self.msg("\n".join(friend_chars_online + friend_chars_offline))
   
    def cmd_add(self, targetname):
        self.msg('STUB: Add')

    def cmd_del(self, targetname):
        self.msg('STUB: Del')

    def cmd_optout(self, targetname):
        self.msg('STUB: Optout')
