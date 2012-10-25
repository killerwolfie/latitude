import re
import sys
import os

class TextCanvas():
    """
    This class creanes a text canvass which can be drawn upon.
    Much like how an image is a 2 dimentional array of pixels, this canvas is
    a two dimentional array of characters, and associated Evennia color codes.

    Internally, the canvas is stored as a perfect rectangle, with equal length
    lines, padded with uncolored spaces.  Optionally, the spaces can be
    stripped when the canvas is turned back into a string.  <<== TODO!
    """
    def __init__(self):
        self.canvas = [[]]

    def set_data(self, canvas_string):
        # Explode the supplied strings into a series of chunks split based on where the color codes happen.
        color_explosion = []
        for newline_section in re.split(r'(\n)', canvas_string):
            for percent_section in re.split(r'(%)%', newline_section):
                for bracket_section in re.split(r'(\{)\{', percent_section):
                    for color_section in re.split(r'(%c[fihnxXrRgGyYbBmMcCwW]|\{[nxXrRgGyYbBmMcCwW])', bracket_section):
                        color_explosion.append(color_section)
        # Iterate through the color explosion, identifying which type of chunk it is, and appending to the canvas data as we go.
        current_fg = None
        current_bg = None
        current_attr = None
        for chunk in color_explosion:
            if chunk == '\n':
                # Newlines increment the line number
                self.canvas.append([])
                continue
            percent_c_match = re.search(r'^%c([fihnxXrRgGyYbBmMcCwW])$', chunk)
            if percent_c_match:
                # Assign the current color based on the %c code
                color_code = percent_c_match.group(1)
                if color_code == 'n':
                    current_fg = None
                    current_bg = None
                    current_attr = None
                elif color_code in 'fih':
                    current_attr = color_code
                elif color_code in 'xrgybmcw':
                    current_fg = color_code
                elif color_code in 'XRGYBMCW':
                    current_bg = color_code
                continue
            bracket_match = re.search(r'^\{([nxXrRgGyYbBmMcCwW])$', chunk)
            if bracket_match:
                # Assign the current color based on the { code
                color_code = bracket_match.group(1)
                if color_code == 'n':
                    current_fg = None
                    current_bg = None
                    current_attr = None
                elif color_code in 'xrgybmcw':
                    current_fg = color_code
                    current_attr = None
                elif color_code in 'XRGYBMCW':
                    current_fg = color_code
                    current_attr = 'h'
                continue
            # Process the chunk as ordinary text
            for c in chunk:
                self.canvas[-1].append({'color_fg' : current_fg, 'color_bg' : current_bg, 'color_attr' : current_attr, 'character' : c})
        # Ensure that the canvas data is perfectly rectangular
        # TODO

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
                if char['character'] == '%':
                    retval += '%%'
                elif char['character'] == '{':
                    retval += '{{'
                else:
                    retval += char['character']
            retval += '\n'
        return retval[:-1]

    def draw_string(self, x, y, string_to_draw, fg=None, bg=None, attr=None):
        # TODO: This function currently does not take a color-coded string!  It should be modified to split color codes out, instead of taking fg, bg, and attr.

        # If needed, expand the canvas horizontally
        for i in range((1 + y) - len(self.canvas)):
            self.canvas.append([])
	# If needed, expand the canvas vertically
	for i in range((x + len(string_to_draw)) - len(self.canvas[y])):
	    self.canvas[y].append({'color_fg' : None, 'color_bg' : None, 'color_attr' : None, 'character' : ' '})
	# Apply the drawing
	for i in range(len(string_to_draw)):
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
	    self.canvas[y][x + i] = {'color_fg' : new_fg, 'color_bg' : new_bg, 'color_attr' : new_attr, 'character' : string_to_draw[i]}

    def draw_canvas(self, x, y, canvas_to_draw, left=True, top=True):
        """
	Draws another canvas class into this canvas.
	canvas_to_draw - The supplied canvas to draw on this canvas
	x, y - Coordinates in this canvas, in which to draw the supplied canvas
        left - If True, then x indicates where to put the leftmost column of convas_to_draw,
	       otherwise x indicates the rightmost column
	top - If True, then y represents where to put the topmost row of canvas_to_draw,
	      otherwise y indicates the bottommost row.
	"""
        pass

    def resize(self, x, y, pad_left=False, bad_top=False):
        """
	Resizes the canvas.
	x, y - New size
	pad_left - If True, the
	"""
        pass

    def width(self):
        max_len = 0
        for line in self.canvas:
            if max_len < len(line):
	        max_len = len(line)
        return max_len

    def height(self):
        """
	Returns the number of lines in the canvas.
	"""
        return len(self.canvas)
