from ev import default_cmds
from game.gamesrc.latitude.utils.log import *

class LatitudeCommand(default_cmds.MuxCommand):
    def parse(self):
        super(LatitudeCommand, self).parse()
        # Determine the 'character' and 'player' objects, and set them accordingly
        if hasattr(self.caller, 'player'):
            self.character = self.caller
            self.player = self.caller.player
        elif hasattr(self.caller, 'get_puppet'):
            self.character = self.caller.get_puppet(self.sessid)
            self.player = self.caller
        elif self.caller.player:
            self.character = None
            self.player = None
        # Log the command if configured to do so
        if hasattr(self, 'logged') and self.logged:
            log_info('Logged command by %s: %s%s' % (self.player or self.caller, self.cmdstring, self.raw))
