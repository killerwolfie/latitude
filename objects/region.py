from game.gamesrc.latitude.objects.object import Object
from game.gamesrc.latitude.commands.region.cmdset import RegionCmdSet

class Region(Object):
    """
    This object is a container for areas, and it handles various functions to related to large regions in the game world, such as generating new areas on demand, weather, etc.
    """

    def at_object_creation(self):
        super(Region, self).at_object_creation()
        self.locks.add('call:true()')
        self.cmdset.add(RegionCmdSet, permanent=True)

    def bad(self):
        if self.location:
            return 'region has a location'
        return super(Area, self).bad()

    def return_styled_name(self, looker=None):
        return '{m[' + self.key + ']'

    def get_area(self):
        return None

    def get_region(self):
        return self
