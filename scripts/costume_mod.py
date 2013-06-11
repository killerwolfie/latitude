from game.gamesrc.latitude.scripts.desc_mod import DescMod

class CostumeMod(DescMod):
    """
    Description modifier class
    """
    def at_script_creation(self):
        super(CostumeMod, self).at_script_creation()
        self.key = "attribute_mod"

    def priority(self):
        return self.db.priority or 0

    def modify_appearance(self, appearance):
        if self.bad():
            return appearance
        return self.db.costume_obj.costume_appearance() or appearance

    def modify_aura(self, aura):
        if self.bad():
            return aura
        return self.db.costume_obj.costume_aura() or aura

    def modify_flavor(self, flavor):
        if self.bad():
            return flavor
        return self.db.costume_obj.costume_flavor() or flavor

    def modify_scent(self, scent):
        if self.bad():
            return scent
        return self.db.costume_obj.costume_scent() or scent

    def modify_sound(self, sound):
        if self.bad():
            return sound
        return self.db.costume_obj.costume_sound() or sound

    def modify_texture(self, texture):
        if self.bad():
            return texture
        return self.db.costume_obj.costume_texture() or texture

    def modify_writing(self, writing):
        if self.bad():
            return writing
        return self.db.costume_obj.costume_writing() or writing

    def modify_species(self, species):
        if self.bad():
            return species
        return self.db.costume_obj.costume_species() or species

    def modify_gender(self, gender):
        if self.bad():
            return gender
        return self.db.costume_obj.costume_gender() or gender

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if not self.db.costume_obj:
            return 'no costume object'
        return super(CostumeMod, self).bad()
