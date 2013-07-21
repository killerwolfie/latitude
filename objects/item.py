"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.object import Object

class Item(Object):
    """
    This type of object is similar to the base Object class, except that it's considered inanimate, and something that could potentially be picked up and stored in a character inventory.
    """
    def get_desc_styled_name(self, looker=None):
        return '{g' + self.key
