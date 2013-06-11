from game.gamesrc.latitude.scripts.script import Script

class Mod(Script):
    """
    Base class for status modifying conditions (good or bad)
    """
    def at_script_creation(self):
        super(Mod, self).at_script_creation()
        self.key = "mod"
	self.desc = "<<MODIFIER>>"
	self.interval = 0
	self.persistent = True
        self.locks.add(';'.join([
            'valid:true()', # Used internally, checks whether a character is supposed to have this mod
            'bear:script_obj()' # Checks whether a character bears this mod
        ]))

    def active(self):
        """
        Returns whether this mod is currently active.

        If this returns a false value, other values from the class should not be applied, and may return None.
        """
        if self.bad():
            return False
        return self.access(self.obj, 'bear')

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if not self.obj:
            return "orphaned mod"
        if not self.access(self.obj, 'valid'):
            return "mod is not valid for its object"
        if type(self) is Mod:
            return "script is a base 'Mod' class"
        return super(Mod, self).bad()
