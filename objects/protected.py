"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.object import Object

class Protected(Object):
    """
    This class is used for objects which should not be automatically deleted during area cleanups.
    """
    def bad(self):
        if type(self) is Protected:
            return "object is a base 'Protected' class"
        return None

    def get_desc_styled_name(self, looker=None):
        return '{x![' + self.key + ']!'
