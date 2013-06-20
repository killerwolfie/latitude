"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.item import Item
from game.gamesrc.latitude.struct.mod import Mod

class Equipment(Item, Mod):
    """
    This is the base class for equipment, such as shirts, pants, swords, wicked
    awesome arm mounted laser cannons, etc.
    """
    def bad(self):
        """
        Audits whether the object is corrupted in some way.

        If the object is valid, then None is returned.  If it's broken, then a string
        is returned containing a reason why.
        """
        try:
            equipper = self.db.equipper
            if equipper:
                if not self in equipper.db.equipment:
                    return "character and equipment data conflict"
        except:
            return "exception raised during audit: " + sys.exc_info()[0]


    def equipment_slot(self):
        """
        Returns which 'slot' this equipment occupies.  For example, right
        finger, head, boots, etc.  It's used to ensure that you don't wear
        multiple of the same type of gear.
        """
        # This must be overridden by the equipment subclass.
        raise NotImplemented('equipment base class used directly')

    def at_equip(self, equipper):
        """
        Called when an object is successfully equipped.
        Returning 'False' will prevent the equipping from occuring.
        """
        equipper.msg(self.objsub('You equip &0d.'))

    def at_unequip(self, unequipper):
        """
        Called when an object is sucessfully unequipped.
        Returning 'False' will prevent the equipping from occuring.
        """
        unequipper.msg(self.objsub('You unequip &0d.'))

    def action_use(self, user):
        self.action_equip(user)

    def action_use_on(self, user, targets):
        if len(targets) != 1:
            user.msg('You can only use that on one one thing at a time.')
        target = targets[0]
        if user != target:
            user.msg('You can only use that on yourself.')
        self.action_equip(user)

    def action_equip(self, equipper):
        # Verify permission
        if not self.location or not self.location == equipper:
            equipper.msg('You have to pick it up first.')
            return
        if self in equipper.get_equipment():
            equipper.msg(self.objsub("You're already wearing &0o."))
            return
        this_slot = self.equipment_slot()
        current_equip = equipper.get_equipment(slot=this_slot)
        if len(current_equip) == 1:
            current_equip = list(current_equip)[0]
            equipper.msg(self.objsub("{R[Try '{runequip &1n{R' first.]", current_equip))
            equipper.msg(self.objsub("You're already wearing &1i.", current_equip))
            return
        elif len(current_equip) > 1:
            # Theoretically we could support more than one thing in one slot at some point.
            # Chances are this will never be reached though under sane conditions, so we don't need to be specific.
            equipper.msg("You're already wearing multiple %ss." % (str(this_slot).lower()))
            return
        # Equip object
        result = self.at_equip(equipper)
        if result or result == None:
            self.db.equipper = equipper
            equipper.db.equipment.add(self)

    def action_unequip(self, unequipper):
        # Verify permission
        if not self in unequipper.get_equipment():
            unequipper.msg(self.objsub("You're not wearing &0o."))
            return
        # Unequip object
        result = self.at_unequip(unequipper)
        if result or result == None:
            self.db.equipper = None
            unequipper.db.equipment.remove(self)

    def get_equipper(self):
        """
        Returns who is currently equipping this object.
        """
        if self.bad():
            return None
        return self.db.equipper
