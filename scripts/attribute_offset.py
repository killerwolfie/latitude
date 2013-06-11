from game.gamesrc.latitude.scripts.attribute_mod import AttributeMod

class AttributeOffset(AttributeMod):
    """
    This script indicates that the character object to which its attached has some 'offset attribute' modifier.
    """
    def at_script_creation(self):
        super(AttributeOffset, self).at_script_creation()
        self.key = "attribute_offset"

    def offset(self):
        if self.bad():
            return None
        return self.db.offset or 0

    def stacking(self):
        return self.db.stacking

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if self.db.offset != None and not isinstance(self.db.offset, int):
            return 'non integer offset'
        return super(AttributeOffset, self).bad()
