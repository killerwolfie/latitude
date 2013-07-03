from game.gamesrc.latitude.objects.object import Object
from game.gamesrc.latitude.commands.region.cmdset import RegionCmdSet
from random import choice

class Region(Object):
    """
    This object is a container for areas, and it handles various functions to related to large regions in the game world, such as generating new areas on demand, weather, etc.
    """

    def at_object_creation(self):
        super(Region, self).at_object_creation()
        self.locks.add('call:true()')
        self.locks.add('leave:true()')
        self.cmdset.add(RegionCmdSet, permanent=True)

    def bad(self):
        if self.location:
            return 'region has a location'
        return super(Area, self).bad()

    def get_desc_styled_name(self, looker=None):
        return '{m[' + self.key + ']'

    def get_desc_appearance_name(self, looker=None):
        return ('%cn%ch%cw' + self.key)

    def get_desc_appearance_desc(self, looker=None):
        desc = self.db.desc_appearance
        if desc != None:
            return '%cn' + desc
        else:
            return None

    def get_desc_appearance_contents(self, looker=None):
        return None

    def get_desc_appearance_exits(self, looker=None):
        return '{x[Use "visit" or "wander" to find a specific location]'

    def wander(self, character):
        """
        Send the character to a random area in this region.

        By default this just picks an area at random with an equal chance of giving you any area.
        """
        options = [area for area in self.contents if hasattr(area, 'can_wander_to') and area.can_wander_to(character)]
        character.redirectable_move_to(choice(options))
