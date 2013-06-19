from game.gamesrc.latitude.scripts.equipped_item import EquippedItem

class EquippedCostume(EquippedItem):
    """
    Description modifier class
    """
    def at_script_creation(self):
        super(EquippedCostume, self).at_script_creation()
        self.key = "attribute_mod"

    def desc_mod_source(self):
        equipped_obj = self.db.equipped_obj
        if equipped_obj:
            return equipped_obj.return_styled_name()
        else:
            return '{R???'

    def desc_mod_type(self):
        return '{yCostume'

    def priority(self):
        return self.db.priority or 0

    def mod_appearance(self, appearance):
        return self.db.equipped_obj.costume_appearance()

    def mod_aura(self, aura):
        return self.db.equipped_obj.costume_aura()

    def mod_flavor(self, flavor):
        return self.db.equipped_obj.costume_flavor()

    def mod_scent(self, scent):
        return self.db.equipped_obj.costume_scent()

    def mod_sound(self, sound):
        return self.db.equipped_obj.costume_sound()

    def mod_texture(self, texture):
        return self.db.equipped_obj.costume_texture()

    def mod_writing(self, writing):
        return self.db.equipped_obj.costume_writing()

    def mod_species(self, species):
        return self.db.equipped_obj.costume_species()

    def mod_gender(self, gender):
        return self.db.equipped_obj.costume_gender()
