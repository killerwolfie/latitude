from game.gamesrc.latitude.objects.item import Item

class Stackable(Item):
    """
    This is the base class for items which can be unified into 'stacks', meaning that they have an associated 'quantity' value for each object.
    """
    def basetype_setup(self):
        super(Stackable, self).basetype_setup()
        # By default the quantity is 1
        self.db.quantity = 1
        # Like the properties, the locks of a stackable item should also never be modified.
        self.locks.replace("call:false();get:true();drop:true()")

    def at_object_creation(self):
        self.key = 'Stackable'

    def bad(self):
        # The locks should never change from the default
        if not sorted(str(self.locks).split(';')) == ['call:false()', 'drop:true()', 'get:true()']:
            return 'stackable item has custom locks'
        # There should not be any attributes except for 'quantity'
        for attr in self.get_all_attributes():
            if attr.key != 'quantity':
                return 'stackable item has a non-quantity attribute'
        # Verify the quantity
        if self.db.quantity < 1:
            return 'invalid stackable item quantity'
        # Looks like we're good.
        return super(Stackable, self).bad()

    def get_desc_styled_name(self, looker=None):
        if self.db.quantity and self.db.quantity > 1:
            return super(Stackable, self).get_desc_styled_name(looker=looker) + '{n (%d)' % self.db.quantity
        else:
            return super(Stackable, self).get_desc_styled_name(looker=looker)

    def combine(self, other):
        # Safety/sanity check the combine
        if not type(other) is type(self):
            return False
        if self.bad() or other.bad():
            return False
        # Save the quantity in this object
        self.db.quantity = self.db.quantity + other.db.quantity
        # Delete the other object
        other.delete()
        # Success
        return True

