from ev import CmdSet

from game.gamesrc.latitude.commands.area import look
from game.gamesrc.latitude.commands.default.character import leave

class AreaCmdSet(CmdSet):
    key = "AreaCmdSet"
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
	self.add(leave.CmdLeave)
