"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.equipment import Equipment

class Costume(Equipment):
    """
    This item is a costume, or 'morph'.  Using it while it's in your inventory
    attaches it to yourself, and its description(s) override yours.  Using it again
    (Or removing it from your posession) disables the costume and your descs return to
    normal.
    """
    def equipment_slot(self):
        return 'costume'

    def at_equip(self, equipper):
        """
        Called to perform the actual equip.
        """
        equipper.msg(self.objsub('You wear &0d, and your appearance changes.'))

    def at_unequip(self, unequipper):
        """
        Called to perform the actual unequip.
        """
        unequipper.msg(self.objsub('You remove &0d, and return to your normal appearance.'))

    def mod_desc_source(self):
        """
        Returns a stylized string, typically an object or status condition name, that describes the source of the mod.
        Returns None if this information is meant to be unknown to the user.
        """
        return self.db.mod_desc_source or self.get_desc_styled_name()

    def mod_desc_detail(self):
        """
        Returns a short description of the mod.  (Such as '+10 Stamina' or 'Invisibility', etc.)
        Returns None if this information is meant to be unknown to the user.
        """
        return self.db.mod_desc_detail or '{yCostume'

    def mod_priority(self):
        return self.db.costume_priority or 0

    def mod_appearance(self, appearance):
        return self.db.costume_appearance

    def mod_contents(self, appearance):
        return self.db.costume_contents

    def mod_aura(self, aura):
        return self.db.costume_aura

    def mod_flavor(self, flavor):
        return self.db.costume_flavor

    def mod_scent(self, scent):
        return self.db.costume_scent

    def mod_sound(self, sound):
        return self.db.costume_sound

    def mod_texture(self, texture):
        return self.db.costume_texture

    def mod_writing(self, writing):
        return self.db.costume_writing

    def mod_species(self, species):
        return self.db.costume_species

    def mod_gender(self, gender):
        return self.db.costume_gender

    def mod_speech_name(self, name):
        return self.db.costume_say_name

    def mod_speech_says(self, says):
        return self.db.costume_say_says

    def mod_speech_asks(self, asks):
        return self.db.costume_say_asks

    def mod_speech_exclaims(self, exclaims):
        return self.db.costume_say_exclaims

    def mod_speech_color_name(self, color_name):
        return self.db.costume_say_color_name

    def mod_speech_color_quote(self, color_quote):
        return self.db.costume_say_color_quote

    def mod_speech_color_depth(self, color_depth):
        retval = {}
        for attr in self.get_all_attributes():
            if not attr.key.startswith('costume_say_color_depth'):
                continue
            this_depth = attr.key[23:]
            if not this_depth.isdigit():
                continue
            retval[int(this_depth)] = attr.value
        return retval or None
