from game.gamesrc.latitude.objects.object import LatitudeObject
from ev import Command
import re

class CmdUse(Command):
    """
    Utilize an object, or objects.

    Usage:
      use
      use <obj>
      use <obj> on <obj1, obj2, ... objn>
      use <obj1, obj2, ... objn> on <obj>

    
    """
    key = "use"
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        args = self.args.strip()
        if not args:
            self.caller.msg('Use what?')
            return
        # Split the used from the used_on
        useparts = re.split(r'(?<!,)\s+on\s+', args, 1)
        used = re.split(r',\s*', useparts[0])
        if len(useparts) > 1:
            used_on = re.split(r',\s*', useparts[1])
        else:
            used_on = None
        # Ensure that at least one of used or used_on has only one object (The object which will be called to handle the use)
        if len(used) > 1 and (used_on == None or len(used_on) > 1):
            self.caller.msg("You can't use all that stuff at once.  (See 'help use')")
            return
        # Search out all the objects
        used = [ self.caller.search(item) for item in used ]
        if None in used:
            # Looks like one of the searches failed.  It should have displayed an error to the user, so bail out.
            return
        if used_on:
            used_on = [ self.caller.search(item) for item in used_on ]
            if None in used_on:
                # Looks like one of the searches failed.  It should have displayed an error to the user, so bail out.
                return
        # Determine which object to call for use handling, and cal lit.
        if len(used) == 1:
            if used_on:
                used[0].action_use_on(self.caller, used_on)
            else:
                used[0].action_use(self.caller)
        else:
            used_on[0].action_used_on_by(self.caller, used)
