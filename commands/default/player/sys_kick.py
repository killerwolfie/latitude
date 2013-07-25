from game.gamesrc.latitude.commands.default.character.sys_kick import CmdSysKick as CharacterCmdSysKick

class CmdSysKick(CharacterCmdSysKick):
    """
    @kick - Kick a character out to the region menu

    Usage:
      @kick <character>
        Send a given character back to the region menu.  You must have
        permission to kick the user.  (Typically this means you have to be
        the 'resident' or owner of the room the character is in, but some
        rooms can have special rules for when, or by whom, kicking is
        allowed.)
    """ # FIXME: Copied from character
    def func(self):
        if self.character:
            self.msg("{R[That command isn't available right now]")
        else:
            self.msg("{R[You're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R]")
