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

    def at_equip(self, equipper):
        """
        Called when equipment is sucessfully equipped.
        """
        equipper.msg(self.objsub('You equip &0d.'))

    def at_unequip(self, unequipper):
        """
        Called when equipment is successfully unequipped.
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
        attr_name = 'equipment_' + self.equipment_slot()
        if equipper.get_attribute(attr_name):
            current_equip = equipper.get_attribute(attr_name)
            if current_equip == self:
                equipper.msg(self.objsub("You're already wearing &0o."))
            else:
                equipper.msg(self.objsub("{R[Try '{runequip &1n{R' first.]", current_equip))
                equipper.msg(self.objsub("You're already wering &1i.", current_equip))
            return
        # Equip object
        equipper.set_attribute(attr_name, self)
        self.at_equip(equipper)

    def action_unequip(self, unequipper):
        # Verify permission
        attr_name = 'equipment_' + self.equipment_slot()
        if not unequipper.get_attribute(attr_name) or unequipper.get_attribute(attr_name) != self:
            unequipper.msg(self.objsub("You're not wearing &0o."))
            return
        # Unequip object
        unequipper.set_attribute(attr_name, None)
        self.at_unequip(unequipper)

    def is_equipped_by(self, equipper):
        """
        Returns true if this object is equipped by equipper.
        """
        return equipper.get_attribute('equipment_' + self.equipment_slot()) == self
