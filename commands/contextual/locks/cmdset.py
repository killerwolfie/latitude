from ev import CmdSet

from game.gamesrc.latitude.commands.contextual.locks import lock
from game.gamesrc.latitude.commands.contextual.locks import unlock

class LatitudeCmdsetLocks(CmdSet):
    key = "Deadbost"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
	self.add(lock.CmdLock)
	self.add(unlock.CmdUnlock)
