from ev import CmdSet

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands.default.player import special_channel
from game.gamesrc.latitude.commands.default.player import special_nomatch
from game.gamesrc.latitude.commands.default.player import sys_3who
from game.gamesrc.latitude.commands.default.player import sys_about
from game.gamesrc.latitude.commands.default.player import sys_access
from game.gamesrc.latitude.commands.default.player import sys_ban
from game.gamesrc.latitude.commands.default.player import sys_boot
from game.gamesrc.latitude.commands.default.player import sys_cboot
from game.gamesrc.latitude.commands.default.player import sys_ccreate
from game.gamesrc.latitude.commands.default.player import sys_cdesc
from game.gamesrc.latitude.commands.default.player import sys_cdestroy
from game.gamesrc.latitude.commands.default.player import sys_cemit
from game.gamesrc.latitude.commands.default.player import sys_channel
from game.gamesrc.latitude.commands.default.player import sys_char
from game.gamesrc.latitude.commands.default.player import sys_cset
from game.gamesrc.latitude.commands.default.player import sys_emit
from game.gamesrc.latitude.commands.default.player import sys_examine
from game.gamesrc.latitude.commands.default.player import sys_find
from game.gamesrc.latitude.commands.default.player import sys_friends
from game.gamesrc.latitude.commands.default.player import sys_gametime
from game.gamesrc.latitude.commands.default.player import sys_help
from game.gamesrc.latitude.commands.default.player import sys_imc2chan
from game.gamesrc.latitude.commands.default.player import sys_imcinfo
from game.gamesrc.latitude.commands.default.player import sys_imcpage
from game.gamesrc.latitude.commands.default.player import sys_irc2chan
from game.gamesrc.latitude.commands.default.player import sys_kick
from game.gamesrc.latitude.commands.default.player import sys_last
from game.gamesrc.latitude.commands.default.player import sys_merge
from game.gamesrc.latitude.commands.default.player import sys_newpassword
from game.gamesrc.latitude.commands.default.player import sys_objects
from game.gamesrc.latitude.commands.default.player import sys_page
from game.gamesrc.latitude.commands.default.player import sys_password
from game.gamesrc.latitude.commands.default.player import sys_pref
from game.gamesrc.latitude.commands.default.player import sys_py
from game.gamesrc.latitude.commands.default.player import sys_quell
from game.gamesrc.latitude.commands.default.player import sys_quit
from game.gamesrc.latitude.commands.default.player import sys_reload
from game.gamesrc.latitude.commands.default.player import sys_reset
from game.gamesrc.latitude.commands.default.player import sys_rss2chan
from game.gamesrc.latitude.commands.default.player import sys_say
from game.gamesrc.latitude.commands.default.player import sys_scripts
from game.gamesrc.latitude.commands.default.player import sys_serverload
from game.gamesrc.latitude.commands.default.player import sys_service
from game.gamesrc.latitude.commands.default.player import sys_sethelp
from game.gamesrc.latitude.commands.default.player import sys_shutdown
from game.gamesrc.latitude.commands.default.player import sys_teleport
from game.gamesrc.latitude.commands.default.player import sys_unban
from game.gamesrc.latitude.commands.default.player import sys_wall
from game.gamesrc.latitude.commands.default.player import sys_whereare
from game.gamesrc.latitude.commands.default.player import sys_who

class LatitudeCmdsetPlayer(CmdSet):
    """
    This is set is available to the player when they have no
    character connected to them (i.e. they are out-of-character, ooc).
    """
    key = "Player"
    priority = 10

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        self.add(special_channel.CmdChannel)
        self.add(special_nomatch.CmdNoMatch)
        self.add(sys_3who.CmdSys3Who)
        self.add(sys_about.CmdSysAbout)
        self.add(sys_access.CmdSysAccess)
        self.add(sys_ban.CmdSysBan)
        self.add(sys_boot.CmdSysBoot)
        self.add(sys_cboot.CmdSysCBoot)
        self.add(sys_ccreate.CmdSysChannelCreate)
        self.add(sys_cdesc.CmdSysCdesc)
        self.add(sys_cdestroy.CmdSysCdestroy)
        self.add(sys_cemit.CmdSysCemit)
        self.add(sys_channel.CmdSysChannel)
        self.add(sys_char.CmdSysChar)
        self.add(sys_cset.CmdSysCset)
        self.add(sys_examine.CmdSysExamine)
	self.add(sys_help.CmdSysHelp)
        self.add(sys_emit.CmdSysEmit)
        self.add(sys_find.CmdSysFind)
        self.add(sys_friends.CmdSysFriends)
        self.add(sys_gametime.CmdSysGameTime)
        self.add(sys_imc2chan.CmdSysIMC2Chan)
        self.add(sys_imcinfo.CmdSysIMCInfo)
        self.add(sys_imcpage.CmdSysIMCPage)
        self.add(sys_irc2chan.CmdSysIRC2Chan)
        self.add(sys_kick.CmdSysKick)
        self.add(sys_last.CmdSysLast)
        self.add(sys_merge.CmdSysMerge)
        self.add(sys_newpassword.CmdSysNewPassword)
        self.add(sys_objects.CmdSysObjects)
        self.add(sys_page.CmdSysPage)
        self.add(sys_password.CmdSysPassword)
        self.add(sys_pref.CmdSysPref)
        self.add(sys_py.CmdSysPy)
        self.add(sys_quell.CmdSysQuell)
        self.add(sys_quit.CmdSysQuit)
        self.add(sys_reload.CmdSysReload)
        self.add(sys_reset.CmdSysReset)
        self.add(sys_rss2chan.CmdSysRSS2Chan)
        self.add(sys_say.CmdSysSay)
        self.add(sys_scripts.CmdSysScripts)
        self.add(sys_serverload.CmdSysServerLoad)
        self.add(sys_service.CmdSysService)
        self.add(sys_sethelp.CmdSysSetHelp)
        self.add(sys_shutdown.CmdSysShutdown)
        self.add(sys_teleport.CmdSysTeleport)
        self.add(sys_unban.CmdSysUnban)
        self.add(sys_wall.CmdSysWall)
        self.add(sys_whereare.CmdSysWhereare)
        self.add(sys_who.CmdSysWho)
