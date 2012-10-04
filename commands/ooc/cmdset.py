from ev import CmdSet

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands.ooc import sys_addcom
from game.gamesrc.latitude.commands.ooc import sys_allcom
from game.gamesrc.latitude.commands.ooc import sys_cboot
from game.gamesrc.latitude.commands.ooc import sys_cdesc
from game.gamesrc.latitude.commands.ooc import sys_cdestroy
from game.gamesrc.latitude.commands.ooc import sys_cemit
from game.gamesrc.latitude.commands.ooc import sys_channelcreate
from game.gamesrc.latitude.commands.ooc import sys_channels
from game.gamesrc.latitude.commands.ooc import sys_cset
from game.gamesrc.latitude.commands.ooc import sys_cwho
from game.gamesrc.latitude.commands.ooc import sys_delcom
from game.gamesrc.latitude.commands.ooc import sys_delplayer
from game.gamesrc.latitude.commands.ooc import sys_encoding
from game.gamesrc.latitude.commands.ooc import sys_help
from game.gamesrc.latitude.commands.ooc import sys_ic
from game.gamesrc.latitude.commands.ooc import sys_imc2chan
from game.gamesrc.latitude.commands.ooc import sys_imcinfo
from game.gamesrc.latitude.commands.ooc import sys_imctell
from game.gamesrc.latitude.commands.ooc import sys_irc2chan
from game.gamesrc.latitude.commands.ooc import sys_newpassword
from game.gamesrc.latitude.commands.ooc import sys_ooc
from game.gamesrc.latitude.commands.ooc import sys_ooclook
from game.gamesrc.latitude.commands.ooc import sys_page
from game.gamesrc.latitude.commands.ooc import sys_password
from game.gamesrc.latitude.commands.ooc import sys_quit
from game.gamesrc.latitude.commands.ooc import sys_reload
from game.gamesrc.latitude.commands.ooc import sys_reset
from game.gamesrc.latitude.commands.ooc import sys_rss2chan
from game.gamesrc.latitude.commands.ooc import sys_shutdown

class OOCCmdSet(CmdSet):
    """
    This is set is available to the player when they have no
    character connected to them (i.e. they are out-of-character, ooc).
    """
    key = "OOC"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(sys_addcom.CmdSysAddCom)
        self.add(sys_allcom.CmdSysAllCom)
        self.add(sys_cboot.CmdSysCBoot)
        self.add(sys_cdesc.CmdSysCdesc)
        self.add(sys_cdestroy.CmdSysCdestroy)
        self.add(sys_cemit.CmdSysCemit)
        self.add(sys_channelcreate.CmdSysChannelCreate)
        self.add(sys_channels.CmdSysChannels)
        self.add(sys_cset.CmdSysCset)
        self.add(sys_cwho.CmdSysCWho)
        self.add(sys_delcom.CmdSysDelCom)
        self.add(sys_delplayer.CmdSysDelPlayer)
	self.add(sys_help.CmdSysHelp)
        self.add(sys_encoding.CmdSysEncoding)
        self.add(sys_ic.CmdSysIC)
        self.add(sys_imc2chan.CmdSysIMC2Chan)
        self.add(sys_imcinfo.CmdSysIMCInfo)
        self.add(sys_imctell.CmdSysIMCTell)
        self.add(sys_irc2chan.CmdSysIRC2Chan)
        self.add(sys_newpassword.CmdSysNewPassword)
        self.add(sys_ooc.CmdSysOOC)
        self.add(sys_ooclook.CmdSysOOCLook)
        self.add(sys_page.CmdSysPage)
        self.add(sys_password.CmdSysPassword)
        self.add(sys_quit.CmdSysQuit)
        self.add(sys_reload.CmdSysReload)
        self.add(sys_reset.CmdSysReset)
        self.add(sys_rss2chan.CmdSysRSS2Chan)
        self.add(sys_shutdown.CmdSysShutdown)

