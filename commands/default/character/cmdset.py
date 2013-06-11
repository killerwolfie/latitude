from ev import CmdSet

#from contrib import menusystem, lineeditor
#from contrib import misc_commands
#from contrib import chargen

from game.gamesrc.latitude.commands.default.character import drop
from game.gamesrc.latitude.commands.default.character import equip
from game.gamesrc.latitude.commands.default.character import feel
from game.gamesrc.latitude.commands.default.character import follow
from game.gamesrc.latitude.commands.default.character import get
from game.gamesrc.latitude.commands.default.character import inventory
from game.gamesrc.latitude.commands.default.character import lead
from game.gamesrc.latitude.commands.default.character import listen
from game.gamesrc.latitude.commands.default.character import lock
from game.gamesrc.latitude.commands.default.character import look
from game.gamesrc.latitude.commands.default.character import map
from game.gamesrc.latitude.commands.default.character import pose
from game.gamesrc.latitude.commands.default.character import read
from game.gamesrc.latitude.commands.default.character import say
from game.gamesrc.latitude.commands.default.character import sense
from game.gamesrc.latitude.commands.default.character import smell
from game.gamesrc.latitude.commands.default.character import start
from game.gamesrc.latitude.commands.default.character import stop
from game.gamesrc.latitude.commands.default.character import spoof
from game.gamesrc.latitude.commands.default.character import taste
from game.gamesrc.latitude.commands.default.character import unequip 
from game.gamesrc.latitude.commands.default.character import unlock
from game.gamesrc.latitude.commands.default.character import use
from game.gamesrc.latitude.commands.default.character import whisper

from game.gamesrc.latitude.utils import menusystem

class LatitudeCmdsetCharacter(CmdSet):
    key = "Character"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
	self.add(drop.CmdDrop)
	self.add(equip.CmdEquip)
	self.add(feel.CmdFeel)
	self.add(follow.CmdFollow)
	self.add(get.CmdGet)
	self.add(inventory.CmdInventory)
	self.add(listen.CmdListen)
	self.add(lead.CmdLead)
	self.add(lock.CmdLock)
	self.add(look.CmdLook)
	self.add(map.CmdMap)
	self.add(pose.CmdPose)
	self.add(read.CmdRead)
	self.add(say.CmdSay)
	self.add(sense.CmdSense)
	self.add(smell.CmdSmell)
	self.add(start.CmdStart)
	self.add(stop.CmdStop)
	self.add(spoof.CmdSpoof)
	self.add(taste.CmdTaste)
	self.add(unequip.CmdUnequip)
	self.add(unlock.CmdUnlock)
	self.add(use.CmdUse)
	self.add(whisper.CmdWhisper)

        #self.add(menusystem.CmdMenuTest())
        #self.add(lineeditor.CmdEditor())
        #self.add(misc_commands.CmdQuell())

