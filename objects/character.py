from ev import Character
from game.gamesrc.latitude.objects.object import LatitudeObject

class LatitudeCharacter(LatitudeObject, Character):
    """
    The Character is like any normal Object (see example/object.py for
    a list of properties and methods), except it actually implements
    some of its hook methods to do some work:

    at_basetype_setup - always assigns the default_cmdset to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_disconnect - stores the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_post_login - retrieves the character's old location and puts it back
                    on the grid with a "charname has connected" message echoed
                    to the room

    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudeCharacter, self).basetype_setup()
        self.locks.add(";".join([
            "edit_appearance:id(%s)" % (self.dbref), # Allows users to modify this object's 'appearance' description
            "edit_aura:id(%s)" % (self.dbref),       # Allows users to modify this object's 'aura' description
            "edit_flavor:id(%s)" % (self.dbref),     # Allows users to modify this object's 'flavor' description
            "edit_scent:id(%s)" % (self.dbref),      # Allows users to modify this object's 'scent' description
            "edit_sound:id(%s)" % (self.dbref),      # Allows users to modify this object's 'sound' description
            "edit_texture:id(%s)" % (self.dbref),    # Allows users to modify this object's 'texture' description
            "edit_writing:id(%s)" % (self.dbref),    # Allows users to modify this object's 'writing' description
            "edit_gender:id(%s)" % (self.dbref),     # Allows users to modify this object's 'gender' description
            "edit_species:id(%s)" % (self.dbref),    # Allows users to modify this object's 'species' description
            "follow:none()",                         # Who can automatically follow
            "lead:none()",                           # Who can automatically lead
            "get:false()",                           # Nobody can pick up the character
            "drop:true()",                           # Let's hope this doesn't get called
            "call:false()",                          # No commands can be called on character from outside
        ]))

    def at_after_move(self, source_location):
        if self.db.prefs_automap == None or self.db.prefs_automap:
	    self.execute_cmd('map')
        self.execute_cmd('look')

    def at_post_login(self):
        super(LatitudeCharacter, self).at_post_login() # For now call the default handler which unstows the character

        self.at_after_move(None) # Logging in counts as moving into a location.  Perform all the looking around and position tracking involved in that.
