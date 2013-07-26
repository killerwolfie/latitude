from ev import default_cmds, utils

class LatitudeCommand(default_cmds.MuxCommand):
    def parse(self):
        super(LatitudeCommand, self).parse()
        # Determine the 'character' and 'player' objects, and set them accordingly
        if utils.inherits_from(self.caller, "src.objects.objects.Object"):
            self.character = self.caller
            self.player = self.caller.player
        elif utils.inherits_from(self.caller, "src.players.player.Player"):
            self.character = self.caller.get_puppet(self.sessid)
            self.player = self.caller
        else:
            self.character = None
            self.player = None
        # Log the command if configured to do so
        if hasattr(self, 'logged') and self.logged:
            self.msg('STUBLOG: %s%s' % (self.cmdstring, self.raw))
