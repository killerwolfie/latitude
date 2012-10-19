from ev import CmdSet

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands.default.character import drop
from game.gamesrc.latitude.commands.default.character import feel
from game.gamesrc.latitude.commands.default.character import follow
from game.gamesrc.latitude.commands.default.character import get
from game.gamesrc.latitude.commands.default.character import inventory
from game.gamesrc.latitude.commands.default.character import lead
from game.gamesrc.latitude.commands.default.character import listen
from game.gamesrc.latitude.commands.default.character import look
from game.gamesrc.latitude.commands.default.character import map
from game.gamesrc.latitude.commands.default.character import pose
from game.gamesrc.latitude.commands.default.character import read
from game.gamesrc.latitude.commands.default.character import say
from game.gamesrc.latitude.commands.default.character import ooc
from game.gamesrc.latitude.commands.default.character import sense
from game.gamesrc.latitude.commands.default.character import smell
from game.gamesrc.latitude.commands.default.character import spoof
from game.gamesrc.latitude.commands.default.character import sys_about
from game.gamesrc.latitude.commands.default.character import sys_access
from game.gamesrc.latitude.commands.default.character import sys_ban
from game.gamesrc.latitude.commands.default.character import sys_batchcode
from game.gamesrc.latitude.commands.default.character import sys_batchcommands
from game.gamesrc.latitude.commands.default.character import sys_boot
from game.gamesrc.latitude.commands.default.character import sys_copy
from game.gamesrc.latitude.commands.default.character import sys_cpattr
from game.gamesrc.latitude.commands.default.character import sys_create
from game.gamesrc.latitude.commands.default.character import sys_debug
from game.gamesrc.latitude.commands.default.character import sys_desc
from game.gamesrc.latitude.commands.default.character import sys_destroy
from game.gamesrc.latitude.commands.default.character import sys_dig
from game.gamesrc.latitude.commands.default.character import sys_emit
from game.gamesrc.latitude.commands.default.character import sys_examine
from game.gamesrc.latitude.commands.default.character import sys_find
from game.gamesrc.latitude.commands.default.character import sys_gohome
from game.gamesrc.latitude.commands.default.character import sys_help
from game.gamesrc.latitude.commands.default.character import sys_home
from game.gamesrc.latitude.commands.default.character import sys_link
from game.gamesrc.latitude.commands.default.character import sys_cmdsets
from game.gamesrc.latitude.commands.default.character import sys_lock
from game.gamesrc.latitude.commands.default.character import sys_mvattr
from game.gamesrc.latitude.commands.default.character import sys_name
from game.gamesrc.latitude.commands.default.character import sys_nick
from game.gamesrc.latitude.commands.default.character import sys_objects
from game.gamesrc.latitude.commands.default.character import sys_open
from game.gamesrc.latitude.commands.default.character import sys_perm
from game.gamesrc.latitude.commands.default.character import sys_py
from game.gamesrc.latitude.commands.default.character import sys_script
from game.gamesrc.latitude.commands.default.character import sys_scripts
from game.gamesrc.latitude.commands.default.character import sys_serverload
from game.gamesrc.latitude.commands.default.character import sys_service
from game.gamesrc.latitude.commands.default.character import sys_setattribute
from game.gamesrc.latitude.commands.default.character import sys_sethelp
from game.gamesrc.latitude.commands.default.character import sys_setobjalias
from game.gamesrc.latitude.commands.default.character import sys_teleport
from game.gamesrc.latitude.commands.default.character import sys_time
from game.gamesrc.latitude.commands.default.character import sys_tunnel
from game.gamesrc.latitude.commands.default.character import sys_typeclass
from game.gamesrc.latitude.commands.default.character import sys_unban
from game.gamesrc.latitude.commands.default.character import sys_unlink
from game.gamesrc.latitude.commands.default.character import sys_wall
from game.gamesrc.latitude.commands.default.character import sys_who
from game.gamesrc.latitude.commands.default.character import sys_wipe
from game.gamesrc.latitude.commands.default.character import taste
from game.gamesrc.latitude.commands.default.character import use

class LatitudeCmdsetCharacter(CmdSet):
    key = "Character"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
	self.add(drop.CmdDrop)
	self.add(feel.CmdFeel)
	self.add(follow.CmdFollow)
	self.add(get.CmdGet)
	self.add(inventory.CmdInventory)
	self.add(listen.CmdListen)
	self.add(lead.CmdLead)
	self.add(look.CmdLook)
	self.add(map.CmdMap)
	self.add(ooc.CmdOOC)
	self.add(pose.CmdPose)
	self.add(read.CmdRead)
	self.add(say.CmdSay)
	self.add(sense.CmdSense)
	self.add(smell.CmdSmell)
	self.add(spoof.CmdSpoof)
        self.add(sys_about.CmdSysAbout)
        self.add(sys_access.CmdSysAccess)
        self.add(sys_ban.CmdSysBan)
        self.add(sys_batchcode.CmdSysBatchCode)
        self.add(sys_batchcommands.CmdSysBatchCommands)
        self.add(sys_boot.CmdSysBoot)
        self.add(sys_copy.CmdSysCopy)
        self.add(sys_cpattr.CmdSysCpAttr)
        self.add(sys_create.CmdSysCreate)
        self.add(sys_debug.CmdSysDebug)
        self.add(sys_desc.CmdSysDesc)
        self.add(sys_destroy.CmdSysDestroy)
        self.add(sys_dig.CmdSysDig)
        self.add(sys_emit.CmdSysEmit)
        self.add(sys_examine.CmdSysExamine)
        self.add(sys_find.CmdSysFind)
	self.add(sys_gohome.CmdSysGoHome)
        self.add(sys_help.CmdSysHelp)
	self.add(sys_home.CmdSysHome)
        self.add(sys_link.CmdSysLink)
        self.add(sys_cmdsets.CmdSysCmdSets)
        self.add(sys_lock.CmdSysLock)
        self.add(sys_mvattr.CmdSysMvAttr)
        self.add(sys_name.CmdSysName)
        self.add(sys_nick.CmdSysNick)
        self.add(sys_objects.CmdSysObjects)
        self.add(sys_open.CmdSysOpen)
        self.add(sys_perm.CmdSysPerm)
        self.add(sys_py.CmdSysPy)
        self.add(sys_script.CmdSysScript)
        self.add(sys_scripts.CmdSysScripts)
        self.add(sys_serverload.CmdSysServerLoad)
        self.add(sys_service.CmdSysService)
        self.add(sys_setattribute.CmdSysSetAttribute)
        self.add(sys_sethelp.CmdSysSetHelp)
        self.add(sys_setobjalias.CmdSysSetObjAlias)
        self.add(sys_teleport.CmdSysTeleport)
        self.add(sys_time.CmdSysTime)
        self.add(sys_tunnel.CmdSysTunnel)
        self.add(sys_typeclass.CmdSysTypeclass)
        self.add(sys_unban.CmdSysUnban)
        self.add(sys_unlink.CmdSysUnLink)
        self.add(sys_wall.CmdSysWall)
        self.add(sys_who.CmdSysWho)
        self.add(sys_wipe.CmdSysWipe)
	self.add(taste.CmdTaste)
	self.add(use.CmdUse)

        #self.add(menusystem.CmdMenuTest())
        #self.add(lineeditor.CmdEditor())
        #self.add(misc_commands.CmdQuell())

