from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import default_cmds, search_object
import re

class CmdStart(default_cmds.MuxCommand):
    """
    start
       'Start' an object.

    Usage:
      start <name>
          Start a specific character or object.
    """
    key = "start"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.caller
        args = self.args.lower()
        if args:
            target = character.search(args)
            if not target:
                return # Search function takes care of error messages
            target.action_start(character)
        else:
            character.action_start(character)
