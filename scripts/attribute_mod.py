from game.gamesrc.latitude.scripts.mod import Mod

class AttributeMod(Mod):
    """
    Base class for attribute modifiers (offsets, multipliers, etc.)
    """
    def at_script_creation(self):
        super(AttributeMod, self).at_script_creation()
        self.key = "attribute_mod"

    def attribute(self):
        """
        Return the name of the attribute modified by this script
        """
        if self.bad():
            return None
        return self.db.attribute

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if type(self) is AttributeMod:
            return 'base AttributeMod class used directly'
        return super(AttributeMod, self).bad()
