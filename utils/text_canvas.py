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

    def evennia_import(self, canvas_string):
        """
        Replaces the data in the canvas with the data supplied in a string.
        Evennia color codes are parsed, so that the resulting canvas should contain exactly what you would see if you printed the string with msg()
        This (and all other) routines require and when appopriate attempt to ensure that the canvas is perfectly rectangular.

        canvas_string - The string to import
        """
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
        self.resize(self.width(), self.height())

    def evennia_export(self):
        """
        Produces a string representation of the contents of the canvas, with color codes suitable for sending to Evennia's 'msg' call.
        """
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

    def draw_string(self, x, y, string_to_draw, transparent_background=False, transparent_spaces=False):
        string_canvas = TextCanvas()
        string_canvas.evennia_import(string_to_draw)
        self.draw_canvas(x, y, string_canvas, transparent_background, transparent_spaces)

    def draw_canvas(self, x, y, canvas_to_draw, transparent_background=False, transparent_spaces=False):
        """
	Draws another canvas class into this canvas.
        Any overflow will not be drawn, so ensure that the canvas is properly resize()'d beforehand if needed.

	canvas_to_draw - The supplied canvas to draw on this canvas
	x, y - Coordinates in this canvas, in which to draw the supplied canvas
	"""
        # Ensure the underlying data is perfectly square by resizing the canvas to its current size
        self.resize(self.width(), self.height())
        # Apply the canvas
        for y_in, line_in in enumerate(canvas_to_draw.canvas):
            for x_in, char_in in enumerate(line_in):
                # Attempt to ensure that we don't overflow the canvas
                if y_in + y >= len(self.canvas):
                    continue
                if x_in + x >= len(self.canvas[y_in + y]):
                    continue
                # Skip this character if spaces are transparent
                if transparent_spaces and char_in['character'] == ' ':
                    continue
                # Modify the character if background colors are transparent
                if transparent_background:
                    char_in['color_bg'] = self.canvas[y_in + y][x_in + x]['color_bg']
                # Draw the character
                self.canvas[y_in + y][x_in + x] = char_in

    def resize(self, x, y, x_pad_before=False, y_pad_before=False):
        """
	Resizes the canvas.

	x, y - New size
	"""
        self.canvas += [ [] for line in range(y - len(self.canvas)) ] # Pad vertically (If applicable)
        del self.canvas[(y + 1):] # Truncate vertically (If applicable)
        for line in self.canvas:
            line += [ {'color_fg' : None, 'color_bg' : None, 'color_attr' : None, 'character' : ' '} for char in range(x - len(line)) ] # Pad horizontally (If applicable)
            del line[(x + 1):] # Truncate horizontally (If applicable)

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
