from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdLook(LatitudeCommand):
    """
    look - Use your sense of sight

    Usage:
      look
      look ['at'] <obj>
        Visually observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ['l']
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('appearance')

    def percieve(self, sense, default_obj=None):
        """
        Handle the percieving.
        """
        character = self.character
        args = self.args
        if args.lower().startswith('at '):
            args = args[3:].strip()
        if args:
            # Use search to handle duplicate/nonexistant results.
            looking_at_obj = character.search(args, use_nicks=True)
            if not looking_at_obj:
                return
        elif default_obj:
            looking_at_obj = default_obj
        else:
            looking_at_obj = character.location
            if not looking_at_obj:
                self.msg("You have no location to percieve!")
                return
        # Get the object's description
        self.msg(getattr(looking_at_obj, 'get_desc_'+ sense)(looker=character))
        # the object's at_desc() method.
	if sense == 'appearance':
	    sense_callback = 'at_desc'
	else:
	    sense_callback = 'at_desc_' + sense
        getattr(looking_at_obj, sense_callback)(looker=character)
