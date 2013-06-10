from ev import search_script
from ev import search_player
import re
import random
import sys
import os
import time

from ev import Room as EvenniaRoom
from ev import Exit as EvenniaExit
from game.gamesrc.latitude.objects.object import Object
from game.gamesrc.latitude.utils import evennia_color

class Room(Object, EvenniaRoom):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(Room, self).basetype_setup()
        self.locks.add(";".join([
            "rename:resident()",          # Allows users to rename this object
            "edit:resident()",            # Allows users to modify this object (required in addition to what is being edited, specifically)
            "edit_appearance:resident()", # Allows users to modify this object's 'appearance' description
            "edit_aura:resident()",       # Allows users to modify this object's 'aura' description
            "edit_flavor:resident()",     # Allows users to modify this object's 'flavor' description
            "edit_scent:resident()",      # Allows users to modify this object's 'scent' description
            "edit_sound:resident()",      # Allows users to modify this object's 'sound' description
            "edit_texture:resident()",    # Allows users to modify this object's 'texture' description
            "edit_writing:resident()",    # Allows users to modify this object's 'writing' description
            "drop_into:resident()",       # Allows users to drop objects into this room (Requires 'drop' permission on the object as well.)
            "place_exit:resident()",      # Allows users to create exits in this room 
            "call:true()",                # Allow to call commands on this object (Used by the system itself)
            "puppet:false()",             # It would be weird to puppet a room ...
            "get:false()",                # Holding an room doesn't really make sense
            "drop:false()",               # Dropping an room doesn't really make sense
        ]))

    def at_object_creation(self):
        self.db.attr_gender = 'Object'

    def return_styled_name(self, looker):
        return '{w' + self.key

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
	retval = super(Room, self).return_scent(looker)
        visible = (con for con in self.contents if con != looker)
	for con in visible:
	    if con.db.desc_scent and not isinstance(con, EvenniaExit):
	        retval += '\n[%s]\n%s\n' % (con.key, con.db.desc_scent)
	# Return the scents of everything in the room as well
	return retval

    def return_texture(self, looker):
        """
	Returns the scent description of the object.
	"""
	return super(Room, self).return_texture(looker)

    def return_flavor(self, looker):
        """
	Returns the scent description of the object.
	"""
	return super(Room, self).return_flavor(looker)

    def return_sound(self, looker):
        """
	Returns the scent description of the object.
	"""
	retval = super(Room, self).return_sound(looker)
	# Return the sounds of things in the room at random
        visible = (con for con in self.contents if con != looker)
	for con in visible:
	    if con.db.desc_sound and not isinstance(con, EvenniaExit) and random.random() < 0.25:
	        retval += '\n  %s' % (con.db.desc_sound)
	return retval

    def return_aura(self, looker):
        """
	Returns the scent description of the object.
	"""
	retval = super(Room, self).return_aura(looker)
	# Return the auras of everything in the room as well
        visible = (con for con in self.contents if con != looker)
	for con in visible:
	    if con.db.desc_aura and not isinstance(con, EvenniaExit):
	        retval += '\n[%s]\n%s\n' % (con.key, con.db.desc_aura)
	return retval

    def return_writing(self, looker):
        """
	Returns the scent description of the object.
	"""
	return super(Room, self).return_writing(looker)

    # ----- Maps -----
    def return_map(self, print_location=False, mark_self=True, mark_friends_of=None):
        try:
	    # Grab the time at which this call was made, so if the call takes a while it doesn't drift our 'idle time' calculations
	    now = time.time()
	    # Grab the map
	    area = self.get_area()
            if not area:
                return None
	    region = area.get_region()
            if not region:
                return None
            area_map_num = self.db.area_map_num
            if area_map_num == None:
                return None
	    map_data = area.get_attribute('maps')[self.db.area_map_num]['map_data']
            if not map_data:
                return None
            # Parse the map data's color codes and create a canvas
            canvas = evennia_color.EvenniaColorCanvas()
            canvas.evennia_import(map_data)
            # Generate a list of marks, and associated legend entries.
	    marks = {}
	    # TODO: poi_marks ?
	    if mark_self and self.db.area_map_x and self.db.area_map_y:
	        location = (self.db.area_map_x, self.db.area_map_y)
		marker = {'type' : 'Location', 'legend' : None, 'prio' : 10}
	        if location in marks:
		    marks[location].append(marker)
		else:
		    marks[location] = [ marker ]
            if mark_friends_of:
	        if mark_friends_of.player:
		    mark_friends_of = mark_friends_of.player
                for friend in mark_friends_of.get_friend_characters(online_only=True):
                    if friend.location and friend.location.db.area_id == area.dbref and friend.location.db.area_map_x and friend.location.db.area_map_y:
                        location = (friend.location.db.area_map_x, friend.location.db.area_map_y)
                        friend_owner = friend.get_owner()
                        # Determine the best prio
                        if friend.sessions:
                            prio = friend.sessions[0].cmd_last_visible - now
                        elif friend_owner:
                            prio = time.mktime(friend_owner.user.last_login.timetuple()) - now
                        else:
                            prio = float('-inf')
                        # Add the marker
                        marker = {'type' : 'Friend', 'legend' : friend.key, 'prio' : prio}
                        if location in marks:
                            marks[location].append(marker)
                        else:
                            marks[location] = [ marker ]
            # Make sure all the marks are sorted
	    for location in marks.keys():
	        marks[location].sort(key=lambda item: item['prio'], reverse=True)
	    # Place the marks on the map, and generate the legend
            number_markers = [
                '%ch%cg1',
                '%ch%cy2',
                '%ch%cc3',
                '%ch%cm4',
                '%ch%cb5',
            ]
            location_marker = '%crX'
	    legend_remaining = 10
	    legend = ''
	    for location, mark in sorted(marks.items(), key=lambda mark_item: mark_item[1][0]['prio'], reverse=True):
                # Take the item with the highest priority and determine its type of marker
                if mark[0]['type'] == 'Location':
		    marker = location_marker
		    do_legend = False
		elif number_markers:
	            marker = number_markers.pop(0)
		    do_legend = True
		else:
		    # We're out of number markers.  Reduce the remaining quota to 0.
		    legend_remaining = min(0, legend_remaining)
		    marker = None
		    do_legend = True # We want to do the legend even though it won't append to the string, so it tracks how '(# more...)' entries.
		# Make the actual mark
                if marker and legend_remaining > 0 or mark[0]['prio'] >= 0: # If there is no marker to place, or we're drawing an optional (prio < 0) mark without remaining legend space, then skip
		    canvas.draw_string(location[0], location[1], marker, transparent_background=True)
		# Extract the legend items
		if do_legend:
		    legend_items = [item['legend'] for item in mark if item['legend'] != None]
		    if legend_items:
			if marker and legend_remaining > 0: # We're not out of markers, and we're not out of our legend item quota
			    legend += marker + ') '
			    if len(legend_items) <= legend_remaining:
				legend += ', '.join(legend_items)
			    else:
				legend += ', '.join(legend_items[:legend_remaining])
			    legend += ' '
			legend_remaining -= len(legend_items)
	    if legend_remaining < 0:
	        legend += '%cn(' + str(0 - legend_remaining) + ' more...)'

	    # Grab and print the output
            retval = canvas.evennia_export()
	    if print_location:
	        retval += '\n' + ('{bRegion:{n %s {bArea:{n %s {bRoom:{n %s' % (region.db.name, area.db.name, self.key)).center(canvas.width() + 12) # 12 = Number of color escape characters
	    if legend:
		    retval += '\n' + legend
	    return retval
	except ValueError as e:
	    # Looks like we blew it.
	    filename = os.path.split(sys.exc_info()[2].tb_frame.f_code.co_filename)[1]
            line = sys.exc_info()[2].tb_lineno
	    return '{R[Error displaying map (%s:%d): %s]{n' % (filename, line, str(e))

    def get_area(self):
        area_id = self.db.area_id
        if area_id:
            # Sanity check the area_id first
            if area_id[0] != '#' or not area_id[1:].isdigit():
                area_id = None
        if area_id:
            return(search_script(area_id)[0])
        else:
            return(None)

    # ---- Object based string substitution ----
    # A - Absolute Pronoun
    def objsub_a(self):
        if self.db.objsub_a:
	    return(str(self.db.objsub_a))
	return("this room's")

    # O - Objective Pronoun
    def objsub_o(self):
        if self.db.objsub_o:
	    return(str(self.db.objsub_o))
	return('this room')

    # P - Posessive Pronoun
    def objsub_p(self):
        if self.db.objsub_p:
	    return(str(self.db.objsub_p))
	return("this room's")

    # R - Reflexive Pronoun
    def objsub_r(self):
        if self.db.objsub_r:
	    return(str(self.db.objsub_r))
	return("this room")

    # S - Subjective Pronoun
    def objsub_s(self):
        if self.db.objsub_s:
	    return(str(self.db.objsub_s))
	return("this room")
