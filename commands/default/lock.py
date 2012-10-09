from ev import default_cmds
from game.gamesrc.latitude.objects.exit_deadbolt import LatitudeExitDeadbolt

class CmdLock(default_cmds.MuxCommand):
    """
    lock <object>
    
      Attempt to lock <object>, so it can't be opened or used.
    """

    key = "lock"
    locks = "cmd:all()"
    help_category = "Actions"

    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.

    def func(self):
        if not self.args:
	    self.caller.msg('Lock what?')
	    return()
        obj = self.caller.search(self.args)
	if not obj:
	    return()
	if not isinstance(obj, LatitudeExitDeadbolt):
	    self.caller.msg("You can't lock that")
	    return()
	obj.lock(self.caller)
