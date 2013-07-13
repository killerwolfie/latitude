from game.gamesrc.latitude.commands.default.character.sys_kick import CmdSysKick as CharacterCmdSysKick

class CmdSysKick(CharacterCmdSysKick):
    def func(self):
        if self.character:
            self.msg("{R[That command isn't available right now]")
        else:
            self.msg("{R[You're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R]")
