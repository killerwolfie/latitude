from ev import Script as EvenniaScript
from collections import namedtuple

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

    def desc_mod_source(self):
        return None

    def desc_mod_type(self):
        return None

    # ---- Mods ----
    # Some objects will check all attached scripts for 'mods' which change values before they're returned, such as attributes, or descriptions.
    # The script can only advise a change.  It can't control whether the object uses it, in what order, or in what way.
    # These routines should be read only.  They should not do anything that might cause the script object, or any other, to become invalid, or stop (This includes moving objects around, etc.), to avoid race conditions during evaluation.
    def mod_priority(self):
        """
        Returns an advisory integer which may be used to break ties when two scripts want to modify the same thing.
        """
        return 0

    def mod_attr_offset_nostack(self):
        """
        Returns a dictionary of attribute name/offset pairs, intended to not stack, or None for no mod.
        ('Attribute' here means character stat attribute, not to be confused with db or object attributes.)
        """
        return None

    def mod_attr_offset_stack(self):
        """
        Returns a dictionary of attribute name/offset pairs, intended to stack, or None for no mod.
        ('Attribute' here means character stat attribute, not to be confused with db or object attributes.)
        """
        return None

    def mod_attr_multiply_nostack(self):
        """
        Returns a dictionary of attribute name/multiplier pairs, intended to not stack, or None for no mod.
        ('Attribute' here means character stat attribute, not to be confused with db or object attributes.)
        """
        return None

    def mod_attr_multiply_stack(self):
        """
        Returns a dictionary of attribute name/multiplier pairs, intended to stack, or None for no mod.
        ('Attribute' here means character stat attribute, not to be confused with db or object attributes.)
        """
        return None

    def mod_attr_set(self):
        """
        Returns a dictionary of attribute name/new value pairs, intended to overwrite the value of that attribute, or None for no mod.
        ('Attribute' here means character stat attribute, not to be confused with db or object attributes.)
        """
        return None

    def mod_appearance(self, appearance):
        """
        Modifies return_appearance.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_desc(self, appearance):
        """
        Modifies return_appearance_desc.  Returns a new value given an existing one, or None for no mod
        """
        return None

    def mod_appearance_name(self, appearance):
        """
        Modifies return_appearance_name.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_contents_header(self, appearance):
        """
        Modifies return_appearance_contents_header.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_contents(self, appearance):
        """
        Modifies return_appearance_contents.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_exits(self, appearance):
        """
        Modifies return_appearance_exits.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_aura(self, aura):
        """
        Modifies return_aura.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_flavor(self, flavor):
        """
        Modifies return_flavor.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_scent(self, scent):
        """
        Modifies return_scent.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_sound(self, sound):
        """
        Modifies return_sound.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_texture(self, texture):
        """
        Modifies return_texture.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_writing(self, writing):
        """
        Modifies return_writing.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_species(self, species):
        """
        Modifies return_species.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_gender(self, gender):
        """
        Modifies return_gender.  Returns a new value given an existing one, or None for no mod.
        """
        return None

