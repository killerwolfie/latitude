"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.item import LatitudeItem

class LatitudeItemDeadboltKey(LatitudeItem):
    """
    This item is a deadbolt key.  'using' it is a way to call the lock/unlock command classes.
    Any object can be a key for a deadbolt, though, even characters themselves can have key data inside them and can lock/unlock.
    """
