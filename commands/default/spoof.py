from game.gamesrc.latitude.commands.default import say

class CmdSpoof(say.CmdSay):
    """
    spoof - Allows you to make a freeform pose to the room.
    Usage:
      spoof <freeform text>

    Example (If your username is Tom):
      spoof The parade has started! [Tom]
    """
    key = "spoof"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []

    def parse(self):
        super(MuckCommand, self).parse()
        if not self.saycommand:
            self.saycommand = 'spoof'
