from ev import search_script
import re
import random
import sys
import os
import time

from ev import Room
from ev import Exit
from game.gamesrc.latitude.objects.object import LatitudeObject
from game.gamesrc.latitude.utils import evennia_color

class LatitudeRoom(LatitudeObject, Room):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudeRoom, self).basetype_setup()
        self.locks.add(";".join(["puppet:false()", # would be weird to puppet a room ...
                                 "call:true()"])) # characters can call commands in the room

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
    def return_map(self, print_location=False, mark_self=True, mark_friends_of=None):
        if not (self.db.area_id != None and self.db.area_map_num != None):
	    return None
        try:
	    # Grab the time at which this call was made, so if the call takes a while it doesn't drift our 'idle time' calculations
	    now = time.time()
	    # Grab the map
	    area = search_script(self.db.area_id)[0]
	    region = search_script(area.db.region)[0]
	    map_data = area.get_attribute('maps')[self.db.area_map_num]['map_data']
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
		friends = mark_friends_of.db.friends_list
		if friends:
		    for friend in friends:
		        if not friend.sessions: # Offline
			    continue
			if not friend.character: # Not IC.  This will need to be modified to handle multi-character connections.
			    continue
                        friend_char = friend.character
                        if friend_char.location and friend_char.location.db.area_id == area.dbref and friend_char.location.db.area_map_x and friend_char.location.db.area_map_y:
			    location = (friend_char.location.db.area_map_x, friend_char.location.db.area_map_y)
			    if friend.sessions:
			        prio = friend.sessions[0].cmd_last_visible - now
		            else:
			        prio = time.mktime(friend.user.last_login.timetuple()) - now
			    marker = {'type' : 'Friend', 'legend' : friend_char.key, 'prio' : -1}
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
			    legend = marker + ') '
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
