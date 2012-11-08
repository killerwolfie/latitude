from game.gamesrc.latitude.commands.muckcommand import MuckCommand

class CmdLook(MuckCommand):
    """
    look

    Usage:
      look
      look <obj>

    Visually observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ['l']
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        self.percieve('appearance')

    def percieve(self, sense):
        """
        Handle the percieving.
        """
        caller = self.caller
        args = self.args
        if args:
            # Use search to handle duplicate/nonexistant results.
            looking_at_obj = caller.search(args, use_nicks=True)
            if not looking_at_obj:
                return
        else:
            looking_at_obj = caller.location
            if not looking_at_obj:
                caller.msg("You have no location to percieve!")
                return
        # Get the object's description
        caller.msg(getattr(looking_at_obj, 'return_'+ sense)(caller))
        # the object's at_desc() method.
	if sense == 'appearance':
	    sense_callback = 'at_desc'
	else:
	    sense_callback = 'at_desc_' + sense
        getattr(looking_at_obj, sense_callback)(looker=caller)
