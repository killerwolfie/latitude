from game.gamesrc.latitude.scripts.attribute_mod import AttributeMod

class AttributeMultiplier(AttributeMod):
    """
    This script indicates that the character object to which its attached has some 'multiplier attribute' modifier.
    """
    def at_script_creation(self):
        super(AttributeMultiplier, self).at_script_creation()
        self.key = "attribute_multiplier"

    def attribute(self):
        """
        Return the name of the attribute modified by this script
        """
        if self.bad():
            return None
        return self.db.attribute

    def multiplier(self):
        if self.bad():
            return None
        return self.db.multiplier or 1.0

    def stacking(self):
        return self.db.stacking

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if self.db.multiplier != None and not isinstance(self.db.multiplier, float):
            return 'non integer multiplier'
        return super(AttributeMultiplier, self).bad()
