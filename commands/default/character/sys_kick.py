from game.gamesrc.latitude.utils.search import match_character
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysKick(LatitudeCommand):
    """
    @kick - Kick a character out to the region menu

    Usage:
      @kick <character>
        Send a given character back to the region menu.  You must have
        permission to kick the user.  (Typically this means you have to be
        the 'resident' or owner of the room the character is in, but some
        rooms can have special rules for when, or by whom, kicking is
        allowed.)
    """
    key = "@kick"
    locks = "cmd:all()"
    help_category = "General"
    aliases = ['@sweep', 'sweep']
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.character
        if not self.args:
            self.msg('{R[Please specify a character.  See {rhelp %s{R for details]' % (self.key))
            return
        target = match_character(self.args, exact=True)
        if not target:
            self.msg('{R[That character could not be found]')
            return
        if not target.location or not target.location.access(character, 'kick_occupant'):
            return # Access failure should have sent a message
        # Determine the region
        region = target.get_region()
        if not region and target.home:
            region = target.home.get_region()
        if not region:
            default_home = ObjectDB.objects.get_id(settings.CHARACTER_DEFAULT_HOME)
            region = default_home.get_region()
        if not region:
            raise Exception('could not find region')
        # All is well.  Do the kickin'
        target.location.msg_contents("{Y[%s has been kicked from the area by %s]" % (target.key, character.key), exclude=[target, character])
        character.msg('{Y[%s has been kicked from "%s"]' % (target.key, target.location.key))
        target.msg('{Y[You have been kicked from this area by %s]' % (character.key))
        target.move_to(region, redirectable=True, followers=False)
