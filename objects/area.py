from ev import utils

from game.gamesrc.latitude.objects.object import Object

class Area(Object):
    """
    This object is a container for rooms, and it handles various functions relating to a localized vacinity in the game world, such as map data.
    """

    # The basic object locks are fine, because this isn't the kind of object you can pick up, edit, etc.

    def bad(self):
        if not utils.inherits_from(self.location, 'game.gamesrc.latitude.objects.region.Region'):
            return 'area has no region'
        return super(Area, self).bad()

    def return_styled_name(self, looker=None):
        return '{M[' + self.key + ']'

    def get_area(self):
        return self

    def get_region(self):
        return self.location
