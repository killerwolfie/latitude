from game.gamesrc.latitude.scripts.mod import Mod

class DescMod(Mod):
    """
    Description modifier class
    """
    def at_script_creation(self):
        super(DescMod, self).at_script_creation()
        self.key = "attribute_mod"

    def priority(self):
        """
        This returns a value in order to help determine the order to apply multiple DescMods, if applicable.
        """
        return self.db.priority or 0

    def modify_appearance(self, appearance):
        if self.bad():
            return appearance
        return self.has_attribute('appearance') and self.db.appearance or appearance

    def modify_aura(self, aura):
        if self.bad():
            return aura
        return self.has_attribute('aura') and self.db.aura or aura

    def modify_flavor(self, flavor):
        if self.bad():
            return flavor
        return self.has_attribute('flavor') and self.db.flavor or flavor

    def modify_scent(self, scent):
        if self.bad():
            return scent
        return self.has_attribute('scent') and self.db.scent or scent

    def modify_sound(self, sound):
        if self.bad():
            return sound
        return self.has_attribute('sound') and self.db.sound or sound

    def modify_texture(self, texture):
        if self.bad():
            return texture
        return self.has_attribute('texture') and self.db.texture or texture

    def modify_writing(self, writing):
        if self.bad():
            return writing
        return self.has_attribute('writing') and self.db.writing or writing

    def modify_species(self, species):
        if self.bad():
            return species
        return self.has_attribute('species') and self.db.species or species

    def modify_gender(self, gender):
        if self.bad():
            return gender
        return self.has_attribute('gender') and self.db.gender or gender

    def bad(self):
        """
        Checks if the script is corrupt in some way.
        Returns the first problem found with the script, as a string, or None.
        """
        if self.db.appearance != None and not isinstance(self.db.appearance, basestring):
            return 'non-string appearance'
        if self.db.aura != None and not isinstance(self.db.aura, basestring):
            return 'non-string aura'
        if self.db.flavor != None and not isinstance(self.db.flavor, basestring):
            return 'non-string flavor'
        if self.db.scent != None and not isinstance(self.db.scent, basestring):
            return 'non-string scent'
        if self.db.sound != None and not isinstance(self.db.sound, basestring):
            return 'non-string sound'
        if self.db.texture != None and not isinstance(self.db.texture, basestring):
            return 'non-string texture'
        if self.db.writing != None and not isinstance(self.db.writing, basestring):
            return 'non-string writing'
        if self.db.species != None and not isinstance(self.db.species, basestring):
            return 'non-string species'
        if self.db.gender != None and not isinstance(self.db.gender, basestring):
            return 'non-string gender'
        return super(DescMod, self).bad()
