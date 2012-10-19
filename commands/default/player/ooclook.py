from game.gamesrc.latitude.commands.default.character import look
from src.commands.default.muxcommand import MuxCommandOOC
from ev import default_cmds

class CmdOOCLook(MuxCommandOOC, look.CmdLook):
    """
    ooc look

    Usage:
      look

    This is an OOC version of the look command. Since a
    Player doesn't have an in-game existence, there is no
    concept of location or "self". If we are controlling
    a character, pass control over to normal look.

    """

    key = "look"
    aliases = ['@ooclook']
    locks = "cmd:all()"
    help_category = "Actions"

    def func(self):
        "implement the ooc look command"

        if not self.character:
            string = "You are out-of-character (OOC). "
            string += "Use {w@ic{n to get back to the game, {whelp{n for more info."
            self.caller.msg(string)
        else:
            self.caller = self.character # we have to put this back for normal look to work.
            super(CmdOOCLook, self).func()

