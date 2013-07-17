from game.gamesrc.latitude.objects.item import Item

class Prop(Item):
    """
    This type of item is an ornamental prop.  Its purpose is to lie around and look pretty.  Users could potentially edit everything about it, including renaming it.
    """
    def get_desc_styled_name(self, looker=None):
        return '{G' + self.key
