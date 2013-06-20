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
        return self.db.mod_desc_source or self.return_styled_name()

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

    def mod_appearance_desc(self, appearance):
        return self.db.costume_appearance_desc

    def mod_appearance_name(self, appearance):
        return self.db.costume_appearance_name

    def mod_appearance_contents_header(self, appearance):
        return self.db.costume_appearance_contents_header

    def mod_appearance_contents(self, appearance):
        return self.db.costume_appearance_contents

    def mod_appearance_exits(self, appearance):
        return self.db.costume_appearance_exits

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
