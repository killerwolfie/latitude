from ev import default_cmds, search_player
from src.server.sessionhandler import SESSIONS
import shlex

class CmdSysMerge(default_cmds.MuxPlayerCommand):
    """
    @merge

    Merge one or more accounts into another account, transfering in all characters, special bonuses, friends, etc.

    Usage:
      @merge <to account> <from account> [<from account> ...]

    """
    key = "@merge"
    locks = "cmd:perm(command_@merge) or perm(Janitors)"
    aliases = []
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        player_names = shlex.split(self.args)
        if len(player_names) < 2:
            self.msg('Usage: @merge <to account> <from account> [<from account> ...]')
            return
        # Convert the requested account names into players
        players = []
        for player_name in player_names:
            player = search_player(player_name)
            if not player:
                return # The player search should drop an error message
            players.append(player[0])
        # Ensure none of the players are the same
        if len(players) != len(set(players)):
            self.msg("Each player must be different")
            return
        # Ensure that only 'Players' level accounts are involved in the merge
        for player in players:
            if player.permissions != ['Players']:
                self.msg("Each player must be in the 'Players' permissions group")
        # Perform the merge
        to_player = players.pop(0)
        for from_player in players:
            self.merge_players(to_player, from_player)

    def merge_players(self, to_player, from_player):
        self.msg('Merging "%s" into "%s"...' % (from_player, to_player))
        self.msg('  Disconnecting %s (if applicable)...' % (from_player))
        from_player.unpuppet_all()
        for session in SESSIONS.sessions_from_player(from_player):
            from_player.msg('\nYour account has been merged into "%s".\n' % (to_player), sessid=session.sessid)
            from_player.disconnect_session_from_player(session.sessid)
        self.msg('  Transfering characters...')
        transfer_characters = from_player.get_characters()
        if transfer_characters:
            for character in transfer_characters:
                character.set_owner(to_player)
                character.locks.add("puppet:id(%i) or pid(%i) or perm(Janitors)" % (character.id, to_player.id))
                self.msg('    %s' % (character.key))
        else:
            self.msg('    No characters.')
        self.msg('  Transfering friends...')
        if from_player.db.friends_list:
            for friend in from_player.db.friends_list:
                if friend == to_player:
                    # Your other account is friends with you?
                    continue
                self.msg('      ' + friend.key)
                to_player.db.friends_list.add(friend)
        self.msg('  Transfering outstanding friend requests...')
        if from_player.db.friends_requests:
            for request_player in from_player.db.friends_requests:
                if request_player == to_player:
                    # Your other account sent you a friend request?
                    continue
                self.msg('      ' + request_player.key)
                to_player.db.friends_requests.add(request_player)
                # Alter this requesting player's friend roster if needed
                if from_player in request_player.db.friends_list:
                    request_player.db.friends_list.remove(from_player)
                    request_player.db.friends_list.add(to_player)
        self.msg('  Transfering bonuses...')
        if from_player.db.bonus_lat1:
            self.msg('    lat1')
            to_player.db.bonus_lat1 = True
        self.msg('  Deleting "%s"...' % (from_player))
#        from_player.user.delete()
        from_player.delete()
        self.msg('Merge from "%s" to "%s" complete.' % (from_player, to_player))
