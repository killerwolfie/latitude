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
        Called when equipment is sucessfully equipped.
        """
        equipper.msg(self.objsub('You wear &0d, and your appearance changes.'))

    def at_unequip(self, unequipper):
        """
        Called when equipment is successfully unequipped.
        """
        unequipper.msg(self.objsub('You remove &0d, and return to your normal appearance.'))
