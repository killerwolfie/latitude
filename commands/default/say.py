"""
This module contains commands that are used for player communication.

"""

import re
from game.gamesrc.latitude.commands.muckcommand import MuckCommand

# ANSI definitions

ANSI_BEEP = "\07"
ANSI_ESCAPE = "\033"
ANSI_NORMAL = "\033[0m"

ANSI_UNDERLINE = "\033[4m"
ANSI_HILITE = "\033[1m"
ANSI_BLINK = "\033[5m"
ANSI_INVERSE = "\033[7m"
ANSI_INV_HILITE = "\033[1;7m"
ANSI_INV_BLINK = "\033[7;5m"
ANSI_BLINK_HILITE = "\033[1;5m"
ANSI_INV_BLINK_HILITE = "\033[1;5;7m"

# Foreground colors
ANSI_BLACK = "\033[30m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"
ANSI_MAGENTA = "\033[35m"
ANSI_CYAN = "\033[36m"
ANSI_WHITE = "\033[37m"

# Background colors
ANSI_BACK_BLACK = "\033[40m"
ANSI_BACK_RED = "\033[41m"
ANSI_BACK_GREEN = "\033[42m"
ANSI_BACK_YELLOW = "\033[43m"
ANSI_BACK_BLUE = "\033[44m"
ANSI_BACK_MAGENTA = "\033[45m"
ANSI_BACK_CYAN = "\033[46m"
ANSI_BACK_WHITE = "\033[47m"

# Formatting Characters
ANSI_RETURN = "\r\n"
ANSI_TAB = "\t"
ANSI_SPACE = " "

class CmdSay(MuckCommand):
    """
    Usage:
      say <message>

    Talk to those in your current location.

    Use say/help to get extended configuration options.
    """
    key = "say"
    aliases = ['"']
    locks = "cmd:all()"
    help_category = "Actions"

    def func(self):
        message = self.gen_say(self.args)
        if self.caller.location:
            # Call the speech hook on the location
            self.caller.location.at_say(self.caller, message)
            self.caller.location.msg_contents(message, data={"raw":True})
        else:
            self.caller.msg(message, data={"raw":True})

    def gen_say(self, say_string):
        # Determine verb
        if say_string.endswith('?'):
	    verb = self.get_asks()
	elif say_string.endswith('!'):
	    verb = self.get_exclaims()
	else:
	    verb = self.get_says()
	return self.get_color_player() + self.caller.name + ' ' + self.colorize(verb + ', "' + say_string + '"')

    def gen_pose(self, pose_string):
        # TODO: No-space detection
        return(self.get_color_player() + self.caller.name + ' ' + self.colorize(pose_string))

    def get_says(self):
        return "says"

    def get_asks(self):
        return "asks"

    def get_exclaims(self):
        return "exclaims"

    def get_color_depth(self, depth):
        if depth < 1:
	    return ANSI_HILITE + ANSI_BLACK
	elif depth == 1:
	    return ANSI_NORMAL + ANSI_WHITE
	elif depth == 2:
	    return ANSI_HILITE + ANSI_WHITE
	elif depth >= 3:
	    return ANSI_HILITE + ANSI_CYAN

    def get_color_quote(self):
        return ANSI_HILITE + ANSI_RED

    def get_color_player(self):
        return ANSI_HILITE + ANSI_YELLOW

    def colorize(self, say_string):
        retval = u''
        current_color = 0
        last_change = 1
	say_sections = []
        for say_section in say_string.split('"'):
            say_sections.append(self.get_color_depth(current_color) + say_section)
	    if say_section == '':
	        current_color += last_change
	    elif say_section[-1] == ' ':
	        current_color += 1
		last_change = 1
            else:
	        current_color -= 1
		last_change = -1
        return((self.get_color_quote() + '"').join(say_sections))
