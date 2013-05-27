from ev import default_cmds
from ev import utils

class CmdMap(default_cmds.MuxCommand):
    """
    map

    Get an overhead view of your surroundings.

    Usage:
      map
    """

    key = "map"
    locks = "cmd:all()"
    help_category = "Actions"
    arg_regex = r"\s.*?|$"

    def func(self):
        if self.args:
            self.msg('You cartographize "%s"!  (Maybe you meant just "map"?)' % (self.args))
            return
        if self.caller.location:
            if self.caller.get_owner().shows_online():
                self.caller.msg(self.caller.location.return_map(mark_friends_of=self.caller))
            else:
                # If the player is 'hiding' then hide friend markers for privacy
                self.caller.msg(self.caller.location.return_map())
	else:
	    self.caller.msg("You have no location to find on the map!")
