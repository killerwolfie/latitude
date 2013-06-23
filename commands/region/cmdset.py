from ev import CmdSet

from game.gamesrc.latitude.commands.region import look

class RegionCmdSet(CmdSet):
    key = "RegionCmdSet"
    priority = 9
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
