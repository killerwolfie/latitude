from ev import utils
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdMap(LatitudeCommand):
    """
    map - Examine your surroundings topographically

    Usage:
      map
        Get an overhead view of your surroundings.
    """
    key = "map"
    locks = "cmd:all()"
    help_category = "Actions"
    arg_regex = r"\s.*?|$"

    def func(self):
        if self.args:
            self.msg('You cartographize "%s"!  (Maybe you meant just "map"?)' % (self.args))
            return
        if self.character.location:
            if self.character.get_owner().status_online():
                self.msg(self.character.location.get_desc_map(mark_friends_of=self.character))
            else:
                # If the player is 'hiding' then hide friend markers for privacy
                self.msg(self.character.location.get_desc_map())
	else:
	    self.character.msg("You have no location to find on the map!")
