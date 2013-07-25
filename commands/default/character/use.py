from ev import Command
import re
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdUse(Command):
    """
    use - Utilize an object, or objects.

    Usage:
      use <obj>
      use <obj> on <obj1, obj2, ... objn>
      use <obj1, obj2, ... objn> on <obj>
        This is the swiss army knife of action commands.  What it does will depend
        on the objects involved and the configuration of your use command.  You
        can use objects on other objects (even on multiple objects at once), or
        just use an object, in general, with no other objects isvolved.
    """
    key = "use"
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        args = self.args.strip()
        if not args:
            self.msg('Use what?')
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
            self.msg("You can't use all that stuff at once.  (See 'help use')")
            return
        # Search out all the objects
        used = [ self.character.search(item) for item in used ]
        if None in used:
            # Looks like one of the searches failed.  It should have displayed an error to the user, so bail out.
            return
        if used_on:
            used_on = [ self.character.search(item) for item in used_on ]
            if None in used_on:
                # Looks like one of the searches failed.  It should have displayed an error to the user, so bail out.
                return
        # Determine which object to call for use handling, and cal lit.
        if len(used) == 1:
            if used_on:
                used[0].action_use_on(self.character, used_on)
            else:
                used[0].action_use(self.character)
        else:
            used_on[0].action_used_on_by(self.character, used)
