from game.gamesrc.latitude.scripts.script import Script

class Mod(Script):
    """
    Base class for status modifying conditions (good or bad)
    """
    def at_script_creation(self):
        super(Mod, self).at_script_creation()
        self.key = "mod"
	self.interval = 0
	self.persistent = True
        self.locks.add(';'.join([
            'valid:true()' # If this script's 'obj' can not pass this lock, then is_valid() returns false. (And the object self destructs)
        ]))

    def is_valid(self):
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
        if type(self) is Mod:
            return "script is a base 'Mod' class"
        return super(Mod, self).bad()
