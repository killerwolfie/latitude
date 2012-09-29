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
    def at_after_move(self, source_location):
        if self.db.prefs_automap == None or self.db.prefs_automap:
	    self.execute_cmd('map')
        self.execute_cmd('look')
