"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.object import LatitudeObject

class LatitudeItem(LatitudeObject):
    """
    This type of object is similar to the base object class, except that it's considered inanimate, and something that could potentially be picked up and stored in a character inventory.
    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudeItem, self).basetype_setup()
        self.locks.add(";".join(["get:all()",                # pick up object
                                 "call:true()"]))            # allow to call commands on this object
