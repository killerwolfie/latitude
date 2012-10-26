"""
This module contains classes and functions which assist in managing strings which contain Evennia color escape codes.
"""
import re
import sys
import os

class EvenniaColorCanvas():
    """
    This class creanes a text canvass which can be drawn upon.
    Much like how an image is a 2 dimentional array of pixels, this canvas is
    a two dimentional array of characters, and associated Evennia color codes.

    Internally, the canvas is stored as a perfect rectangle, with equal length
    lines, padded with uncolored spaces.
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
                    current_attr = 'h'
                elif color_code in 'XRGYBMCW':
                    current_fg = color_code
                    current_attr = None
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
        string_canvas = EvenniaColorCanvas()
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

def evennia_color_left(string_to_justify, width, dots=False):
    """
    Truncates or pads a string (with spaces) to a desired width, and left justifies each line.
    Color code characters are ignored when padding, or truncating, so that the on screen length (after color parsing) matches the supplied width.

    string_to_justify - A copy of this string is returned, with its contents modified as requested
    width - The desired width of the string.  This isn't the same as the length of the string, because the operation is performed separately on every line.
    signal_trunc - If true, then if any line is truncated, the last three characters will be replaced with '...' to signal that the line was shortened.
    """
    # Truncate the string (If required)
    if dots:
        truncated_string = evennia_color_trunc_dots(string_to_justify, width)
    else:
        truncated_string = evennia_color_trunc(string_to_justify, width)
    # Pad with spaces (If required)
    truncated_string += u' ' * (width - evennia_color_len(truncated_string))
    # Return the result
    return truncated_string
        
def evennia_color_center(string_to_justify, width, dots=False):
    """
    Truncates or pads a string (with spaces) to a desired width, and centers each line.
    Color code characters are ignored when padding, or truncating, so that the on screen length (after color parsing) matches the supplied width.

    string_to_justify - A copy of this string is returned, with its contents modified as requested
    width - The desired width of the string.  This isn't the same as the length of the string, because the operation is performed separately on every line.
    signal_trunc - If true, then if any line is truncated, the last three characters will be replaced with '...' to signal that the line was shortened.
    """
    # Truncate the string (If required)
    if dots:
        truncated_string = evennia_color_trunc_dots(string_to_justify, width)
    else:
        truncated_string = evennia_color_trunc(string_to_justify, width)
    # Left pad with spaces (If required)
    truncated_string = u' ' * ((width - evennia_color_len(truncated_string)) / 2) + truncated_string
    # Right pad with spaces (If required)
    truncated_string += u' ' * (width - evennia_color_len(truncated_string))
    # Return the result
    return truncated_string

def evennia_color_right(string_to_justify, width, dots=False):
    """
    Truncates or pads a string (with spaces) to a desired width, and left justifies each line.
    Color code characters are ignored when padding, or truncating, so that the on screen length (after color parsing) matches the supplied width.

    string_to_justify - A copy of this string is returned, with its contents modified as requested
    width - The desired width of the string.  This isn't the same as the length of the string, because the operation is performed separately on every line.
    signal_trunc - If true, then if any line is truncated, the last three characters will be replaced with '...' to signal that the line was shortened.
    """
    # Truncate the string (If required)
    if dots:
        truncated_string = evennia_color_trunc_dots(string_to_justify, width)
    else:
        truncated_string = evennia_color_trunc(string_to_justify, width)
    # Pad with spaces (If required)
    truncated_string = u' ' * (width - evennia_color_len(truncated_string)) + truncated_string
    # Return the result
    return truncated_string

def evennia_color_trunc_dots(string_to_truncate, width):
    """
    Like evennia_color_trunc, this function truncates a string, compensating for evenna color codes, but if truncation was required, the last three characters are replaced with '...'
    Like evennia_color_trunc, this also doesn't compensate for newlines, just counts them as any other character
    """
    if evennia_color_len(string_to_truncate) > width:
        if width <= 3:
            # Do what we can with the space provided
            return evennia_color_trunc(string_to_truncate, 0) + (u'.' * width)
        else:
            return evennia_color_trunc(string_to_truncate, width - 3) + '...'
    else:
        return evennia_color_trunc(string_to_truncate, width)

def evennia_color_trunc(string_to_truncate, width):
    """
    Truncates a string to a specified length, compensating for any evennia color codes that may be present in the string.
    Does not compensate for newlines, just counts them as any other character.
    """
    # FIXME: Maybe this should determine what the final color code is, in the string, and ensure that the truncated string still ends in that color code.
    #        Might be a bit excessive, though, because users of the function can feel free to append whatever code they want to the end.
    if width <= 0:
        width = 0
    width_remaining = width
    retval = u''
    for percent_section in re.split(r'(%%)', string_to_truncate):
        for bracket_section in re.split(r'(\{\{)', percent_section):
            for color_section in re.split(r'(%c[fihnxXrRgGyYbBmMcCwW]|\{[nxXrRgGyYbBmMcCwW])', bracket_section):
                # Check if we need to ignore the length of this section (because it's a color code)
                if re.search(r'^(%c[fihnxXrRgGyYbBmMcCwW]|\{[nxXrRgGyYbBmMcCwW])$', color_section):
                    retval += color_section
                    continue
                # Calculate the length of this section
                if color_section == '{{' or color_section == '%%':
                    section_length = 1
                else:
                    section_length = len(color_section)
                # Check if we've reached our allotment (If this is changed to > instead of >=, then trailing color codes will make it through)
                if section_length >= width_remaining: # We've reached the end of our allotment
                    retval += color_section[:width_remaining]
                    return retval
                # Append the stringd 
                retval += color_section
                width_remaining -= section_length
    # We got to the end without hitting the cap
    return retval

def evennia_color_len(string_to_measure):
    """
    Returns the length of a string, not counting Evennia color codes
    """
    return len(evennia_color_strip(string_to_measure))

def evennia_color_strip(string_to_strip):
    """
    Strips all Evennia color codes from a string
    """
    clean_string = u''
    for bracket_section in re.split(r'(\{)\{', string_to_strip):
        for percent_section in re.split(r'(%)%', bracket_section):
            clean_string += re.sub(r'(%c[fihnxXrRgGyYbBmMcCwW]|\{[nxXrRgGyYbBmMcCwW])', '', percent_section)
    return clean_string
