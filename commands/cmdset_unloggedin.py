from ev import CmdSet, Command
from ev import default_cmds

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    This is an example of how to overload the command set of the
    unloggedin commands, defined in
    src/commands/default/cmdset_unloggedin.py.

    Here we copy everything by calling the parent, but you can
    copy&paste any combination of the default command to customize
    your default set. Next you change settings.CMDSET_UNLOGGEDIN to
    point to this class.
    """
    key = "Unloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        # calling setup in src.commands.default.cmdset_unloggedin
        super(UnloggedinCmdSet, self).at_cmdset_creation()

        #
        # any commands you add below will overload the default ones.
        #
