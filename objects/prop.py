from game.gamesrc.latitude.objects.item import Item

class Prop(Item):
    """
    This type of item is an ornamental prop.  Its purpose is to lie around and look pretty.  Users could potentially edit everything about it, including renaming it.
    """
    pass
#    def get_desc_appearance_name(self, looker=None):
#        name = self.get_desc_styled_name(looker=looker)
#        if not self.db.canon:
#            name += ' {B[Non-canon]'
#        return name

