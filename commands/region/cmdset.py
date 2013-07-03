from ev import CmdSet

from game.gamesrc.latitude.commands.region import look
from game.gamesrc.latitude.commands.default.character import visit
from game.gamesrc.latitude.commands.default.character import wander

class RegionCmdSet(CmdSet):
    key = "RegionCmdSet"
    priority = 29
    mergetype = "Replace"
    key_mergetypes = {
        'Player' : 'Union',
    }
    no_exits = True
    no_objs = True
    no_channels = False

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
	self.add(look.CmdLook)
        self.add(visit.CmdVisit)
        self.add(wander.CmdWander)
