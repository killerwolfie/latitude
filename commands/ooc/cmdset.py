from ev import CmdSet, Command
from ev import default_cmds

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

class OOCCmdSet(default_cmds.OOCCmdSet):
    """
    This is set is available to the player when they have no
    character connected to them (i.e. they are out-of-character, ooc).
    """
    key = "OOC"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_ooc
        super(OOCCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
