from ev import CmdSet, Command
from ev import default_cmds

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands.default import map
from game.gamesrc.latitude.commands.default import whospecies
from game.gamesrc.latitude.commands.default import lock_unlock
from game.gamesrc.latitude.commands.default import sys_lock

class DefaultCmdSet(default_cmds.DefaultCmdSet):
    key = "DefaultMUX"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_default
        super(DefaultCmdSet, self).at_cmdset_creation()

        #
        # any commands you add below will overload the default ones.
        #
	self.add(map.CmdMap)
	self.add(whospecies.CmdWhospecies)
	self.add(lock_unlock.CmdLock)
	self.add(lock_unlock.CmdUnlock)
	self.add(sys_lock.CmdSysLock)

        #self.add(menusystem.CmdMenuTest())
        #self.add(lineeditor.CmdEditor())
        #self.add(misc_commands.CmdQuell())

