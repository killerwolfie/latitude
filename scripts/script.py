from ev import Script as EvenniaScript

class Script(EvenniaScript):
    """
    Latitude base class for Scripts
    """
    def at_script_creation(self):
        super(Script, self).at_script_creation()

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if type(self) is Script:
            return "script is a base 'Script' class"
        return None
