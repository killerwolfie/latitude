from game.gamesrc.latitude.scripts.attribute_mod import AttributeMod

class AttributeSet(AttributeMod):
    """
    This script indicates that the character object to which its attached has some 'set attribute' modifier.
    """
    def at_script_creation(self):
        super(AttributeSet, self).at_script_creation()
        self.key = "attribute_set"

    def value(self):
        if self.bad():
            return None
        return self.db.value

    def priority(self):
        return self.db.priority or 0

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if self.db.value != None and not isinstance(self.db.value, int):
            return 'non integer value'
        return super(AttributeSet, self).bad()
