from ev import Script as EvenniaScript

class Script(EvenniaScript):
    """
    Latitude base class for Scripts
    """
    def at_script_creation(self):
        super(Script, self).at_script_creation()

    def is_valid(self):
        if type(self) is Script:
            # This is a base Script class
            return False
        return True

    def bad(self):
        """
        Audits whether the script is corrupted in some way, and should be flagged for
        auditing.

        If the script is valid, then None is returned.  If it's broken, then a string
        is returned containing a reason why.
        """
        if type(self) is Script:
            return "script is a base 'Script' class"
        return None

    def desc_script(self):
        # If a traditional desc has been specified, use that by default
        if self.desc:
            return self.desc
        # Second choice default: A description of the mod that this script provides
#        mod_source = self.desc_mod_source()
#        mod_type = self.desc_mod_type()
#        if mod_source and mod_type:
#            return '{C%s{C: %s' % (mod_source, mod_type)
        return ''
