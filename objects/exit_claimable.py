from game.gamesrc.latitude.objects.exit_deadbolt import ExitDeadbolt

class ExitClaimable(ExitDeadbolt):
    def at_object_creation(self):
        super(ExitClaimable, self).at_object_creation()
