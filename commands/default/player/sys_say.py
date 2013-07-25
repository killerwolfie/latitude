from game.gamesrc.latitude.commands.default.character.sys_say import CmdSysSay as CharacterCmdSysSay

class CmdSysSay(CharacterCmdSysSay):
    """
    @say - Speak out-of-character
    
    Usage:
      @say <message>
      @say :<pose>
        Speak or pose with an Out of Character marker. Use this to make sure
        people can tell you're not roleplaying.

        Also, this is not an in-game action, so it doesn't trigger any 'say'
        sensitive events.

    See {whelp say{n, and {whelp pose{n for more details.
    """ # FIXME: Copied from character
    def func(self):
        if self.character:
            self.msg("{R[That command isn't available right now]")
        else:
            self.msg("{R[You're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R]")
