from game.gamesrc.latitude.objects.exit_deadbolt import LatitudeExitDeadbolt

class LatitudeExitClaimable(LatitudeExitDeadbolt):
    def at_object_creation(self):
        super(LatitudeExitClaimable, self).at_object_creation()
