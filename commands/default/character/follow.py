from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import Object, Character, search_object
import re
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdFollow(LatitudeCommand):
    """
    follow - Start following a character or object

    Usage:
      follow <character/object>
        Starts automatically following another character or object.

    To stop following, use 'stop', or move away from your leader.
    See {whelp stop{n for more information.
    """
    key = "follow"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = ['ride', 'hopon']
    arg_regex = r"\s.*?|$"

    def func(self):
        if not self.args:
            self.msg('Follow what?')
            return
        follower = self.character
        leader = follower.search(self.args)
        if follower == leader:
            leader.msg("You march to the beat of your own drum.")
            return
        if not leader:
            return # Error message is handled by the search call
        if not isinstance(leader, Object):
            follower.msg("You can't follow that!")
            return
        if follower.db.follow_following:
            follower.msg("{Y[Try \"{ystop{Y\" to stop following, first.]")
            follower.msg("You're already following %s." % (follower.db.follow_following.key))
            return
        # Start following, if we have permissions.
        if not leader.access(follower, 'follow') and not (leader.db.follow_pending and leader.db.follow_pending_tolead and follower in leader.db.follow_pending):
            # Looks like it's not going to happen.  If we're dealing with a character, give them a chance to give permission
            if isinstance(leader, Character):
                # TODO: ALREADY WAITING
                # Warn the user that existing requests are being cleared
                if follower.db.follow_pending:
                    if follower.db.follow_pending_tolead:
                        follower.msg('You no longer want to lead %s' % (conj_join([char.key for char in follower.db.follow_pending], 'and')))
                    else:
                        follower.msg('You no longer want to follow %s' % (follower.db.follow_pending.key))
                # Set the new request
                follower.db.follow_pending = leader
                follower.db.follow_pending_tolead = False
                # Alert both parties
                leader.msg('{Y[Use "{ylead %s{Y" to lead.]' % (follower.key))
                leader.msg('%s wants to follow you.' % (follower.key))
                follower.msg('You wait for %s to lead you.' % (leader.key))
                return
            # It's not a character.  Fail out.
            self.msg("You can't follow that!")
            return
        # Start following
        follower.db.follow_following = leader
        follower.msg('You start following %s.' % (leader.key))
        leader.msg('%s starts following you.' % (follower.key))
        # Clear existing follow/lead requests if needed.
        if follower.db.follow_pending and follower.db.follow_pending != leader:
            if follower.db.follow_pending_tolead:
                follower.msg("It seems you're now too busy to lead %s." % (conj_join([char.key for char in follower.db.follow_pending], 'and')))
            else:
                follower.msg("It seems you're now too busy to follow %s." % (leader.db.follow_pending.key))
        del follower.db.follow_pending
        del follower.db.follow_pending_tolead
        if leader.db.follow_pending and leader.db.follow_pending_tolead and follower in leader.db.follow_pending:
            leader.db.follow_pending.remove(follower)
            if not leader.db.follow_pending:
                del leader.db.follow_pending
                del leader.db.follow_pending_tolead
