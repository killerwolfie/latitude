from ev import search_script
import re

from ev import Room
from game.gamesrc.latitude.objects.object import LatitudeObject

class LatitudeRoom(LatitudeObject, Room):
    def return_appearance(self, looker):
        return ('%cn%ch%cw' + self.key + '\n' + super(LatitudeRoom, self).return_appearance(looker))

    def generate_map(self):
        if not (self.db.area_id != None and self.db.area_map_num != None):
	    return None

        try:
	    # Grab the map
	    area = search_script('area_' + str(self.db.area_id))[0]
	    map_data = area.get_attribute('maps')[self.db.area_map_num]['map_data']

            # Add in the X (clearing and rebuilding the map)
	    if self.db.area_map_x and self.db.area_map_y:
		orig_map_lines = map_data.splitlines()
		map_data = u''

		x = 1
		y = 1
		mark_placed = False

		for map_line in orig_map_lines:
		    if y == self.db.area_map_y:
		        line_sections = re.split(r'(?<!\\)(%c[fihnxXrRgGyYbBmMcCwW])', map_line)
			map_line = u''
			fg_at_mark = None
			bg_at_mark = None
			attr_at_mark = None
		        for line_section in line_sections:
			    if not line_section:
			        continue
                            color_code_match = re.search(r'^%c([fihnxXrRgGyYbBmMcCwW])$', line_section)
                            if color_code_match:
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
                            else:
			        x += len(line_section)
				if (not mark_placed) and x > self.db.area_map_x:
				    mark_location = len(line_section) - ( x - self.db.area_map_x )
				    mark = '%cn%crX%cn'
				    if attr_at_mark:
				        mark += '%c' + attr_at_mark
				    if fg_at_mark:
				        mark += '%c' + fg_at_mark
				    if bg_at_mark:
				        mark += '%c' + bg_at_mark
				    line_section = line_section[:mark_location] + mark + line_section[mark_location + 1:]
				    mark_placed = True
		            map_line += line_section
	            map_data += map_line + u'\n'
		    y += 1
	    
	    # Return the map
	    return map_data.rstrip('\n')
	except Exception as e:
	    # Looks like we blew it.
	    return '%cr[Error displaying map: ' + str(e) + ']%cn'
