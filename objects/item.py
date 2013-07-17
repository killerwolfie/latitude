"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.object import Object

class Item(Object):
    """
    This type of object is similar to the base Object class, except that it's considered inanimate, and something that could potentially be picked up and stored in a character inventory.
    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(Item, self).basetype_setup()
        self.locks.add(";".join([
            "get:true()",              # Allows users to pick up the object 
            "drop:true()",             # Allows users to put down the object (Requires 'drop_into' at your location as well)
            "edit:holds()",            # Allows users to modify this object (required in addition to what is being edited, specifically)
            "edit_appearance:holds()", # Allows users to modify this object's 'appearance' description
            "edit_aura:holds()",       # Allows users to modify this object's 'aura' description
            "edit_flavor:holds()",     # Allows users to modify this object's 'flavor' description
            "edit_scent:holds()",      # Allows users to modify this object's 'scent' description
            "edit_sound:holds()",      # Allows users to modify this object's 'sound' description
            "edit_texture:holds()",    # Allows users to modify this object's 'texture' description
            "edit_writing:holds()",    # Allows users to modify this object's 'writing' description
            "call:false()",            # allow to call commands on this object (Used by the system itself)
        ]))

    def get_desc_styled_name(self, looker=None):
        return '{g' + self.key
