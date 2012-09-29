from ev import CmdSet, Command
from ev import default_cmds

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands import map
from game.gamesrc.latitude.commands import whospecies

class DefaultCmdSet(default_cmds.DefaultCmdSet):
    """
    This is an example of how to overload the default command
    set defined in src/commands/default/cmdset_default.py.

    Here we copy everything by calling the parent, but you can
    copy&paste any combination of the default command to customize
    your default set. Next you change settings.CMDSET_DEFAULT to point
    to this class.
    """
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

        #self.add(menusystem.CmdMenuTest())
        #self.add(lineeditor.CmdEditor())
        #self.add(misc_commands.CmdQuell())

