from ev import search_script
import re
import random
import sys
import os

from ev import Room
from ev import Exit
from game.gamesrc.latitude.objects.object import LatitudeObject

class LatitudeRoom(LatitudeObject, Room):
    def at_object_creation(self):
        self.db.attr_gender = 'Object'
	self.db.pronoun_absolute = "this room's"
	self.db.pronoun_subjective = "this room"
	self.db.pronoun_objective = "this room"
	self.db.pronoun_posessive = "this room's"
	self.db.pronoun_reflexive = "this room"
        self.db.situational_name = "this room"

    def return_appearance_name(self, looker):
        return ('%cn%ch%cw' + self.key)

    def return_appearance_desc(self, looker):
        desc = self.db.desc_appearance
        if desc != None:
            return('%cn' + desc)
        else:
            return(None)

    def return_scent(self, looker):
        """
	Returns the scent description of the object.
	"""
	retval = super(LatitudeRoom, self).return_scent(looker)
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
	for con in visible:
	    if con.db.desc_scent and not isinstance(con, Exit):
	        retval += '\n[%s]\n%s\n' % (con.key, con.db.desc_scent)
	# Return the scents of everything in the room as well
	return retval

    def return_texture(self, looker):
        """
	Returns the scent description of the object.
	"""
	return super(LatitudeRoom, self).return_texture(looker)

    def return_flavor(self, looker):
        """
	Returns the scent description of the object.
	"""
	return super(LatitudeRoom, self).return_flavor(looker)

    def return_sound(self, looker):
        """
	Returns the scent description of the object.
	"""
	retval = super(LatitudeRoom, self).return_sound(looker)
	# Return the sounds of things in the room at random
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
	for con in visible:
	    if con.db.desc_sound and not isinstance(con, Exit) and random.random() < 0.25:
	        retval += '\n  %s' % (con.db.desc_sound)
	return retval

    def return_aura(self, looker):
        """
	Returns the scent description of the object.
	"""
	retval = super(LatitudeRoom, self).return_aura(looker)
	# Return the auras of everything in the room as well
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
	for con in visible:
	    if con.db.desc_aura and not isinstance(con, Exit):
	        retval += '\n[%s]\n%s\n' % (con.key, con.db.desc_aura)
	return retval

    def return_writing(self, looker):
        """
	Returns the scent description of the object.
	"""
	return super(LatitudeRoom, self).return_writing(looker)

    # ----- Maps -----
    def generate_map(self, print_location=False, mark_self=True, mark_friends_of=None):
        if not (self.db.area_id != None and self.db.area_map_num != None):
	    return None
        try:
	    # Grab the map
	    area = search_script(self.db.area_id)[0]
	    region = search_script(area.db.region)[0]
	    map_data = area.get_attribute('maps')[self.db.area_map_num]['map_data']
            # Parse the map data's color codes and create a canvas
            canvas = TextCanvas()
            canvas.set_data(map_data)
	    if mark_self and self.db.area_map_x and self.db.area_map_y:
                canvas.draw(self.db.area_map_x, self.db.area_map_y, "X", attr=None, fg='r', bg='?')
            if mark_friends_of:
	        if mark_friends_of.player:
		    mark_friends_of = mark_friends_of.player
	        friends = mark_friends_of.db.friends_list
		if friends:
		    friend_markers = [
		        {'character' : '1', 'attr' : 'h', 'fg' : 'g', 'bg' : '?'},
		        {'character' : '2', 'attr' : 'h', 'fg' : 'y', 'bg' : '?'},
		        {'character' : '3', 'attr' : 'h', 'fg' : 'c', 'bg' : '?'},
		        {'character' : '4', 'attr' : 'h', 'fg' : 'm', 'bg' : '?'},
		        {'character' : '5', 'attr' : 'h', 'fg' : 'b', 'bg' : '?'},
		    ]
		    friend_legend = ''
		    for friend in friends:
		        if not friend.sessions: # Offline
			    continue
		        if not friend.character:
			    continue
			friend_char = friend.character
		        if friend_char.location and friend_char.location.db.area_id == area.dbref and friend_char.location != self and friend_char.location.db.area_map_x and friend_char.location.db.area_map_y:
			    friend_marker = friend_markers.pop(0)
                            canvas.draw(friend_char.location.db.area_map_x, friend_char.location.db.area_map_y, friend_marker['character'], attr=friend_marker['attr'], fg=friend_marker['fg'], bg=friend_marker['bg'])
                            friend_legend += '%cn%c' + friend_marker['attr'] + '%c' + friend_marker['fg'] + friend_marker['character'] + ') ' + friend.name + ' '
			    if not friend_markers: # No more markers to place
			        break
            retval = canvas.get_data()
	    if print_location:
	        retval += '\n' + ('{bRegion:{n %s {bArea:{n %s {bRoom:{n %s' % (region.db.name, area.db.name, self.key)).center(canvas.width() + 12) # 12 = Number of color escape characters
	    if mark_friends_of and friend_legend:
	        retval += '\n' + friend_legend
	    return retval
	except ValueError as e:
	    # Looks like we blew it.
	    filename = os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]
            line = sys.exc_info()[2].tb_lineno
	    return '{R[Error displaying map (%s:%d): %s]{n' % (filename, line, str(e))

class TextCanvas():
    def __init__(self):
        self.canvas = []

    def set_data(self, canvas_string):
        self.canvas = []
	for string_line in canvas_string.split('\n'):
	    canvas_line = []
	    line_sections = re.split(r'(?<!\\)(%c[fihnxXrRgGyYbBmMcCwW])', string_line)
	    fg_at_mark = None
	    bg_at_mark = None
	    attr_at_mark = None
	    for line_section in line_sections:
		if not line_section:
		    continue
		color_code_match = re.search(r'^%c([fihnxXrRgGyYbBmMcCwW])$', line_section)
		if color_code_match: # Color code section
		    color_code = color_code_match.group(1)
		    if color_code == 'n':
			fg_at_mark = None
			bg_at_mark = None
			attr_at_mark = None
		    elif color_code in 'fih':
			attr_at_mark = color_code
		    elif color_code in 'xrgybmcw':
			fg_at_mark = color_code
		    elif color_code in 'XRGYBMCW':
			bg_at_mark = color_code
	        else: # Text data section
		    for character in line_section:
		        canvas_line.append({
			    'character' : character,
			    'color_fg' : fg_at_mark,
			    'color_bg' : bg_at_mark,
			    'color_attr' : attr_at_mark,
			})
            self.canvas.append(canvas_line)

    def get_data(self):
        retval = u''
        current_fg = None
        current_bg = None
        current_attr = None
        for line in self.canvas:
            for char in line:
                if char['color_fg'] != current_fg or char['color_bg'] != current_bg or char['color_attr'] != current_attr:
                    current_fg = char['color_fg']
                    current_bg = char['color_bg']
                    current_attr = char['color_attr']
                    retval += '%cn'
                    if current_fg:
                        retval += '%c' + current_fg
                    if current_bg:
                        retval += '%c' + current_bg
                    if current_attr:
                        retval += '%c' + current_attr
                retval += char['character']
            retval += '\n'
        return retval[:-1]

    def draw(self, x, y, draw_string, fg=None, bg=None, attr=None):
        # If needed, expand the canvas horizontally
        for i in range((1 + y) - len(self.canvas)):
            self.canvas.append([])
	# If needed, expand the canvas vertically
	for i in range((x + len(draw_string)) - len(self.canvas[y])):
	    self.canvas[y].append({'color_fg' : None, 'color_bg' : None, 'color_attr' : None, 'character' : ' '})
	# Apply the drawing
	for i in range(len(draw_string)):
	    if fg == '?': # Unchanged
	        new_fg = self.canvas[y][x + i]['color_fg']
            else:
	        new_fg = fg
	    if bg == '?': # Unchanged
	        new_bg = self.canvas[y][x + i]['color_bg']
            else:
	        new_bg = bg
	    if attr == '?': # Unchanged
	        new_attr = self.canvas[y][x + i]['color_attr']
            else:
	        new_attr = attr
	    self.canvas[y][x + i] = {'color_fg' : new_fg, 'color_bg' : new_bg, 'color_attr' : new_attr, 'character' : draw_string[i]}

    def width(self):
        max_len = 0
        for line in self.canvas:
            if max_len < len(line):
	        max_len = len(line)
        return max_len

    def height(self):
        return len(self.canvas)
