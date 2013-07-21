from game.gamesrc.latitude.objects.item import Item

class Prop(Item):
    """
    This type of item is an ornamental prop.  Its purpose is to lie around and look pretty.  Users could potentially edit everything about it, including renaming it.
    """
    def basetype_setup(self):
        super(Prop, self).basetype_setup()
        # By default props can be picked up and dropped.  There can be mechanisms to nail them down later.
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
        ]))
    def get_desc_styled_name(self, looker=None):
        return '{G' + self.key
