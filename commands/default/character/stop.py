from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import default_cmds, search_object
import re

class CmdStop(default_cmds.MuxCommand):
    """
    stop
       Stop following or leading.

    Usage:
      stop
          Stop following your current leader. (Remaining where you are if the
          leader leaves.)

      stop leading
          Stop leading everyone who is currently following you.

      stop <name>
          Stop a specific character or object.

    See 'help follow' and 'help lead' for more details.
    """
    key = "stop"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.caller
        args = self.args.lower()
        if args == 'leading':
            followers = search_object(character, attribute_name='follow_following')
            if not followers:
                character.msg("You're not currently leading anyone.")
                return
            for follower in followers:
                follower.action_stop(character)
        elif args:
            target = character.search(args)
            if not target:
                return # Search function takes care of error messages
            target.action_stop(character)
        else:
            character.action_stop(character)

    def stop_leading(self):
        character = self.caller
