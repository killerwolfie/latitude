"""
This module contains commands that are used for player communication.

"""

import re
from ev import default_cmds

class CmdSay(default_cmds.MuxPlayerCommand):
    """
    Usage:
      say <message>

    Talk to others in your current location.
    """
    key = "say"
    aliases = ['"']
    locks = "cmd:all()"
#    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        message = self.character.speech_say(self.args)
        if self.character.location:
            # Call the speech hook on the location
            self.character.location.at_say(self.character, message)
            self.character.location.msg_contents(message)
        else:
            self.msg(message)
