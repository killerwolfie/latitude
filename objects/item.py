"""
Latitude inanimate object class
"""
from game.gamesrc.latitude.objects.object import Object

class Item(Object):
    """
    This type of object is similar to the base Object class, except that it's considered inanimate, and something that could potentially be picked up and stored in a character inventory.
    """
    def get_desc_styled_name(self, looker=None):
        return '{g' + self.key

    def at_desc_scent(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just smelled &0d.', looker), exclude=[self, looker])

    def at_desc_flavor(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just tasted &0d.', looker), exclude=[self, looker])

    def at_desc_texture(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just felt &0d.', looker), exclude=[self, looker])

