"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.equipment import Equipment
from ev import create_script

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
        Called when equipment is sucessfully equipped.
        """
        script = create_script(typeclass='game.gamesrc.latitude.scripts.costume_mod.CostumeMod', key='costume_mod', obj=equipper)
        script.desc='{nEquipment ({C%s{n): {yCostume' % self.return_styled_name()
        script.locks.add('valid:holds(%s) and equipped(%s)' % (self.dbref, self.dbref))
        script.db.costume_obj = self
        self.db.costume_script = script
        equipper.msg(self.objsub('You wear &0d, and your appearance changes.'))

    def at_unequip(self, unequipper):
        """
        Called when equipment is successfully unequipped.
        """
        costume_script = self.db.costume_script
        if costume_script:
            costume_script.delete()
            costume_script = None
        unequipper.msg(self.objsub('You remove &0d, and return to your normal appearance.'))

    def costume_appearance(self):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_appearance

    def costume_scent(self, looker=None):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_scent

    def costume_texture(self, looker=None):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_texture

    def costume_flavor(self, looker=None):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_flavor

    def costume_sound(self, looker=None):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_sound

    def costume_aura(self, looker=None):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_aura

    def costume_writing(self, looker=None):
        """
	Returns the scent description of a character wearing the costume.
	"""
	return self.db.costume_writing

    def costume_gender(self, looker=None):
        """
        Returns the gender description of a character wearing the costume.  (Typically one word)
        """
        return self.db.costume_gender

    def costume_species(self, looker=None):
        """
        Returns the species description of a character wearing the costume.  (Typically less than 25 characters)
        """
        return self.db.costume_species
