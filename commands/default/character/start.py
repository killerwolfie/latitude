from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import search_object
import re
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdStart(LatitudeCommand):
    """
    start - Start things

    Usage:
      start <name>
        Start a specific character or object.  What this means will vary from
        object to object, or it might not do anything.
    """
    key = "start"
    locks = "cmd:all()"
    help_category = "Actions"
    aliases = []
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.character
        args = self.args.lower()
        if args:
            target = character.search(args)
            if not target:
                return # Search function takes care of error messages
            target.action_start(character)
        else:
            character.action_start(character)
