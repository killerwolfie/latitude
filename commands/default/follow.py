from game.gamesrc.latitude.commands.muckcommand import MuckCommand
from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import search_object
from ev import Object
from ev import Character

class CmdFollow(MuckCommand):
    """
    follow - Start following a character or object.
    Usage:
      follow <character/object>
      follow #auto [<char/obj #1>[ <char/obj #2> ...]]
        Allow others to skip permission checks when they choose to lead you (clears all existing entries).  Use all or none to permit everybody or nobody, respectively.
        If no characters or objects are supplied, it outputs the current values.
      follow #stop
        Stop others from following you.
    """
    key = "follow"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []

    def func(self):
        if 'stop' in self.switches:
            self.stop()
        elif 'auto' in self.switches:
            self.auto()
        else:
            self.follow()

    def stop(self):
        follower = self.caller
        leader = follower.db.follow_following
        # Ensure we're ready to clear the follow
        if not leader:
            follower.msg("You're not currently following anyone.")
            return
        # Clear the follow
        del follower.db.follow_following
        follower.msg('You stop following %s.' % (leader.key))
        leader.msg('%s stops following you.' % (follower.key))

    def follow(self):
        follower = self.caller
        leader = follower.search(self.args)
        if not leader:
            return # Error message is handled by the search call
        if not isinstance(leader, Object):
            follower.msg("You can't follow that!")
            return
        if follower.db.follow_following:
            follower.msg("You're already following %s.  [Use \"follow #stop\" to stop following, first.]" % (follower.db.follow_following.key))
            return
        # Start following, if we have permissions.
        if not leader.access(follower, 'follow') and not (leader.db.follow_pending and follower in leader.db.follow_pending and leader.db.follow_pending_tolead):
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
                leader.msg('%s wants to follow you.  [Use "lead %s" to lead.]' % (follower.key, follower.key))
                follower.msg('You wait for %s to lead you.' % (leader.key))
                return
            # It's not a character.  Fail out.
            self.caller.msg("You can't follow that!")
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
