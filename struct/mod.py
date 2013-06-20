class Mod(object):
    def mod_desc_source(self):
        """
        Returns a stylized string, typically an object or status condition name, that describes the source of the mod.
        Returns None if this information is meant to be unknown to the user.
        """
        return None

    def mod_desc_detail(self):
        """
        Returns a short description of the mod.  (Such as '+10 Stamina' or 'Invisibility', etc.)
        Returns None if this information is meant to be unknown to the user.
        """
        return None

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

