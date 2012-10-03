from ev import CmdSet
from ev import default_cmds

from game.gamesrc.latitude.commands.unloggedin import connect
from game.gamesrc.latitude.commands.unloggedin import create
from game.gamesrc.latitude.commands.unloggedin import help
from game.gamesrc.latitude.commands.unloggedin import look
from game.gamesrc.latitude.commands.unloggedin import quit

class UnloggedinCmdSet(CmdSet):
    key = "Unloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(connect.CmdUnconnectedConnect)
	self.add(create.CmdUnconnectedCreate)
	self.add(help.CmdUnconnectedHelp)
	self.add(look.CmdUnconnectedLook)
	self.add(connect.CmdUnconnectedConnect)
