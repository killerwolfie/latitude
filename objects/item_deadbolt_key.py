"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.item import LatitudeItem

class LatitudeItemDeadboltKey(LatitudeItem):
    """
    This item is a deadbolt key.  'using' it is a way to call the lock/unlock command classes.
    Any object can be a key for a deadbolt, though, even characters themselves can have key data inside them and can lock/unlock.
    """
    def action_use_on(self, user, targets):
        if self.db.deadbolt_key == None:
            user.msg('This key is a blank.')
            return
        for target in targets:
            # First ensure this target matches this lock
            if not target.access(self, 'lock'): # Using 'self' instead of the user.  The user would check all the keys the guy has.  We just want to check this one.
                user.msg("This isn't the right key for %s." % target.return_situational_name())
                continue
            # Perform the lock/unlock based on whether the user can currently traverse the exit
            if target.access(user, 'traverse'):
                target.action_lock(user)
            else:
                target.action_unlock(user)
