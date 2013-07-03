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

    def desc_script(self):
        # If a traditional desc has been specified, use that by default
        if self.desc:
            return self.desc
        # Second choice default: A description of the mod that this script provides
        mod_source = self.desc_mod_source()
        mod_type = self.desc_mod_type()
        if mod_source and mod_type:
            return '{C%s{C: %s' % (mod_source, mod_type)
        return None
