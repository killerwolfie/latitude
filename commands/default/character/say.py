"""
This module contains commands that are used for player communication.

"""

import re
from ev import default_cmds

color_names = {
    'black' : '%cx',
    'red' : '%cr',
    'green' : '%cg',
    'yellow' : '%cy',
    'blue' : '%cb',
    'magenta' : '%cm',
    'cyan' : '%cc',
    'white' : '%cw',
    'bold' : '%ch',
    'hilight' : '%ch',
    'hilite' : '%ch',
}

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
        message = self.gen_say(self.args)
        if self.character.location:
            # Call the speech hook on the location
            self.character.location.at_say(self.character, message)
            self.character.location.msg_contents(message)
        else:
            self.msg(message)

    def gen_say(self, say_string):
        # Determine verb
        if say_string.endswith('?'):
	    verb = self.get_asks()
	elif say_string.endswith('!'):
	    verb = self.get_exclaims()
	else:
	    verb = self.get_says()
	return self.get_color_name() + self.character.name + ' ' + self.colorize(verb + ', "' + say_string + '"')

    def gen_pose(self, pose_string):
        if [chk for chk in ["'s ", '-', ', ', ': ', ' '] if pose_string.startswith(chk)]:
            return(self.get_color_name() + self.character.name + self.colorize(pose_string))
        return(self.get_color_name() + self.character.name + ' ' + self.colorize(pose_string))

    def get_says(self):
        return "says"

    def get_asks(self):
        return "asks"

    def get_exclaims(self):
        return "exclaims"

    def parse_color(self, desc):
        retval = ''
	for name in desc.split(','):
	    if name in color_names:
	        retval += color_names[name]
        if retval:
	    retval = '%cn' + retval # Default to normal
	return retval

    def get_color_depth(self, depth):
        if self.character.get_attribute('say_color_depth' + str(depth)):
	    return self.parse_color(self.character.get_attribute('say_color_depth' + str(depth)))
        if depth < 1:
	    return '%cn%cc'
	elif depth == 1:
	    return '%cn%cw'
	elif depth == 2:
	    return '%cn%cw'
	elif depth >= 3:
	    return '%cn%cw'

    def get_color_quote(self):
        if self.character.get_attribute('say_color_quote'):
	    return self.parse_color(self.character.get_attribute('say_color_quote'))
	return '%cn%cw'

    def get_color_name(self):
        if self.character.get_attribute('say_color_name'):
	    return self.parse_color(self.character.get_attribute('say_color_name'))
	return '%ch%cc'

    def colorize(self, say_string):
        retval = u''
        current_color = 0
        last_change = 1
	say_sections = []
        for say_section in say_string.replace('%', '%%').replace('{', '{{').split('"'):
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
