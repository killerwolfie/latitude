"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.object import Object

class Container(Object):
    """
    This class is used for objects expected to contain other objects.
    """
    def bad(self):
        if type(self) is Container:
            return "object is a base 'Container' class"
        return None

    def get_desc_styled_name(self, looker=None):
        return '{x<(' + self.key + ')>'
