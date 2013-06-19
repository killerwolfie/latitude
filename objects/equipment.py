"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.item import Item

class Equipment(Item):
    """
    This is the base class for equipment, such as shirts, pants, swords, wicked
    awesome arm mounted laser cannons, etc.
    """
    def equipment_slot(self):
        """
        Returns which 'slot' this equipment occupies.  For example, right
        finger, head, boots, etc.  It's used to ensure that you don't wear
        multiple of the same type of gear.
        """
        # This must be overridden by the equipment subclass.
        raise NotImplemented('equipment base class used directly')

    def do_equip(self, equipper):
        """
        Called to perform the actual equip, by creating the appropriate script, and inform the user.
        """
        raise NotImplemented('equipment base class used directly')

    def do_unequip(self, unequipper):
        """
        Called to perform the actual unequip, by stopping the appropriate script, and inform the user.
        """
        raise NotImplemented('equipment base class used directly')

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
        if self.is_equipped_by(equipper):
            equipper.msg(self.objsub("You're already wearing &0o."))
            return
        current_equip = equipper.get_equipment(self.equipment_slot())
        if len(current_equip) == 1:
            equipper.msg(self.objsub("{R[Try '{runequip &1n{R' first.]", current_equip[0]))
            equipper.msg(self.objsub("You're already wearing &1i.", current_equip[0]))
            return
        elif len(current_equip) > 1:
            # Theoretically we could support more than one thing in one slot at some point.
            # Chances are this will never be reached though under sane conditions, so we don't need to be specific.
            equipper.msg("You're already wearing multiple %ss." % (self.equipment_slot().lower()))
            return
        # Equip object
        self.do_equip(equipper)

    def action_unequip(self, unequipper):
        # Verify permission
        if not self.is_equipped_by(unequipper):
            unequipper.msg(self.objsub("You're not wearing &0o."))
            return
        # Unequip object
        self.do_unequip(unequipper)

    def is_equipped_by(self, equipper):
        """
        Returns true if this object is equipped by equipper.
        """
        # Validate first.  This will make sure everything is kosher
        equipper.scripts.validate()
        # Since no funky states should exist now on any of the equipper's scripts, we don't need to check for them.
        equipment_script = self.db.equipment_script
        if not equipment_script:
            return False
        return equipment_script.obj == equipper
