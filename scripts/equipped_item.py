from game.gamesrc.latitude.scripts.script import Script

class EquippedItem(Script):
    """
    This is a base class for scripts which handle the state of having equipment equipped to your character.
    This script is attached to the character, and refers to the equipment.

    DB Attributes:
        equipped_obj
    """
    def at_script_creation(self):
        super(EquippedItem, self).at_script_creation()
        self.key = "equipped_item"
	self.interval = 0
	self.persistent = True

    def at_stop(self):
        if not self.is_valid() and self.obj:
            if self.db.equipped_obj:
                # The script is dying and it's probably because it's invalid, but the equipped object still exists, and so does the equipper, so warn the equipper.
                self.obj.msg(self.db.equipped_obj.objsub('{r[&0N is no longer equipped]'))
            else:
                # Try our best to warn the user that the item has dropped dead
                self.obj.msg('{r[Some of your equipment seems to have fallen off]')

    def is_valid(self):
        if type(self) is EquippedItem:
            # Direct instance of base class
            return False
        equipper = self.obj
        if not equipper:
            # Orphaned script
            return False
        equipper = equipper.typeclass # TODO: See if fixing Issue #384 in Evennia eliminates the need for this
        equipped_obj = self.db.equipped_obj
        if not equipped_obj:
            # Equipped object gone
            return False
        if not equipped_obj.db.equipment_script == self:
            # Object doesn't agree that we're its script
            return False
        if not equipped_obj.location == equipper:
            # Object is no longer in the equipper's posession
            return False
        return super(EquippedItem, self).is_valid()
