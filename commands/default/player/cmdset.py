from ev import CmdSet

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands.default.player import ooclook
from game.gamesrc.latitude.commands.default.player import special_nomatch
from game.gamesrc.latitude.commands.default.player import sys_3who
from game.gamesrc.latitude.commands.default.player import sys_addcom
from game.gamesrc.latitude.commands.default.player import sys_allcom
from game.gamesrc.latitude.commands.default.player import sys_cboot
from game.gamesrc.latitude.commands.default.player import sys_ccreate
from game.gamesrc.latitude.commands.default.player import sys_cdesc
from game.gamesrc.latitude.commands.default.player import sys_cdestroy
from game.gamesrc.latitude.commands.default.player import sys_cemit
from game.gamesrc.latitude.commands.default.player import sys_channels
from game.gamesrc.latitude.commands.default.player import sys_charcreate
from game.gamesrc.latitude.commands.default.player import sys_cset
from game.gamesrc.latitude.commands.default.player import sys_cwho
from game.gamesrc.latitude.commands.default.player import sys_delcom
from game.gamesrc.latitude.commands.default.player import sys_delplayer
from game.gamesrc.latitude.commands.default.player import sys_encoding
from game.gamesrc.latitude.commands.default.player import sys_friends
from game.gamesrc.latitude.commands.default.player import sys_gametime
from game.gamesrc.latitude.commands.default.player import sys_help
from game.gamesrc.latitude.commands.default.player import sys_ic
from game.gamesrc.latitude.commands.default.player import sys_imc2chan
from game.gamesrc.latitude.commands.default.player import sys_imcinfo
from game.gamesrc.latitude.commands.default.player import sys_imcpage
from game.gamesrc.latitude.commands.default.player import sys_irc2chan
from game.gamesrc.latitude.commands.default.player import sys_last
from game.gamesrc.latitude.commands.default.player import sys_merge
from game.gamesrc.latitude.commands.default.player import sys_newpassword
from game.gamesrc.latitude.commands.default.player import sys_ooc
from game.gamesrc.latitude.commands.default.player import sys_page
from game.gamesrc.latitude.commands.default.player import sys_password
from game.gamesrc.latitude.commands.default.player import sys_pref
from game.gamesrc.latitude.commands.default.player import sys_quell
from game.gamesrc.latitude.commands.default.player import sys_quit
from game.gamesrc.latitude.commands.default.player import sys_reload
from game.gamesrc.latitude.commands.default.player import sys_reset
from game.gamesrc.latitude.commands.default.player import sys_rss2chan
from game.gamesrc.latitude.commands.default.player import sys_shutdown

class LatitudeCmdsetPlayer(CmdSet):
    """
    This is set is available to the player when they have no
    character connected to them (i.e. they are out-of-character, ooc).
    """
    key = "Player"
    priority = -5

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(ooclook.CmdOOCLook)
        self.add(special_nomatch.CmdNoMatch)
        self.add(sys_3who.CmdSys3Who)
        self.add(sys_addcom.CmdSysAddCom)
        self.add(sys_allcom.CmdSysAllCom)
        self.add(sys_cboot.CmdSysCBoot)
        self.add(sys_ccreate.CmdSysChannelCreate)
        self.add(sys_cdesc.CmdSysCdesc)
        self.add(sys_cdestroy.CmdSysCdestroy)
        self.add(sys_cemit.CmdSysCemit)
        self.add(sys_channels.CmdSysChannels)
        self.add(sys_charcreate.CmdSysCharCreate)
        self.add(sys_cset.CmdSysCset)
        self.add(sys_cwho.CmdSysCWho)
        self.add(sys_delcom.CmdSysDelCom)
        self.add(sys_delplayer.CmdSysDelPlayer)
	self.add(sys_help.CmdSysHelp)
        self.add(sys_encoding.CmdSysEncoding)
        self.add(sys_friends.CmdSysFriends)
        self.add(sys_gametime.CmdSysGameTime)
        self.add(sys_ic.CmdSysIC)
        self.add(sys_imc2chan.CmdSysIMC2Chan)
        self.add(sys_imcinfo.CmdSysIMCInfo)
        self.add(sys_imcpage.CmdSysIMCPage)
        self.add(sys_irc2chan.CmdSysIRC2Chan)
        self.add(sys_last.CmdSysLast)
        self.add(sys_merge.CmdSysMerge)
        self.add(sys_newpassword.CmdSysNewPassword)
        self.add(sys_ooc.CmdSysOOC)
        self.add(sys_page.CmdSysPage)
        self.add(sys_password.CmdSysPassword)
        self.add(sys_pref.CmdSysPref)
        self.add(sys_quell.CmdSysQuell)
        self.add(sys_quit.CmdSysQuit)
        self.add(sys_reload.CmdSysReload)
        self.add(sys_reset.CmdSysReset)
        self.add(sys_rss2chan.CmdSysRSS2Chan)
        self.add(sys_shutdown.CmdSysShutdown)

