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
        Modifies get_desc_appearance.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_desc(self, appearance):
        """
        Modifies get_desc_appearance_desc.  Returns a new value given an existing one, or None for no mod
        """
        return None

    def mod_appearance_name(self, appearance):
        """
        Modifies get_desc_appearance_name.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_contents_header(self, appearance):
        """
        Modifies get_desc_appearance_contents_header.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_contents(self, appearance):
        """
        Modifies get_desc_appearance_contents.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_appearance_exits(self, appearance):
        """
        Modifies get_desc_appearance_exits.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_aura(self, aura):
        """
        Modifies get_desc_aura.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_flavor(self, flavor):
        """
        Modifies get_desc_flavor.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_scent(self, scent):
        """
        Modifies get_desc_scent.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_sound(self, sound):
        """
        Modifies get_desc_sound.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_texture(self, texture):
        """
        Modifies get_desc_texture.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_writing(self, writing):
        """
        Modifies get_desc_writing.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_species(self, species):
        """
        Modifies get_desc_species.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_gender(self, gender):
        """
        Modifies get_desc_gender.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_name(self, name):
        """
        Modifies speech_name.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_says(self, says):
        """
        Modifies speech_says.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_asks(self, asks):
        """
        Modifies speech_asks.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_exclaims(self, exclaims):
        """
        Modifies speech_exclaims.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_color_name(self, color_name):
        """
        Modifies speech_color_name.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_color_quote(self, color_quote):
        """
        Modifies speech_color_quote.  Returns a new value given an existing one, or None for no mod.
        """
        return None

    def mod_speech_color_depth(self, color_depth):
        """
        Modifies speech_color_depth.  Returns a new value given an existing one, or None for no mod.
          color_depth - Original value
          depth - Requested depth
        """
        return None
