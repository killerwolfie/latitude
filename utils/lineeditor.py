import sys
import re
from ev import Command, syscmdkeys
from contrib.menusystem import prompt_yesno
from game.gamesrc.latitude.utils import evennia_color
import shlex

# Ensure shlex will work with unicode
if sys.version_info < (2,7,3):
    raise Exception("The Latitude Line Editor module requires Python version 2.7.3 or higher")

VI_HELP_STRING = """
{w--{CText Editor Help{w------------------------------------------------------------{n
<txt>  - any non-command is appended to the end of the buffer.
:  <l> - view buffer or only line <l>
:: <l> - view buffer without line numbers or other parsing (In color if available)
:::    - print a ':' as the only character on the line...
:h     - this help.

:w     - saves the buffer (don't quit)
:wq    - save buffer and quit
:q     - quit, but only if the buffer is unchanged.
:q!    - quit without saving, no questions asked

:u     - (undo) step backwards in undo history
:uu    - (redo) step forward in undo history
:UU    - reset all changes back to initial

:dd <l>     - delete line <n>
:dw <l> <w> - delete word or regex <w> in entire buffer or on line <l>
:DD         - clear buffer

:y  <l>        - yank (copy) line <l> to the copy buffer
:x  <l>        - cut line <l> and store it in the copy buffer
:p  <l>        - put (paste) previously copied line directly after <l>
:i  <l> <txt>  - insert new text <txt> at line <l>. Old line will be shifted down
:r  <l> <txt>  - replace line <l> with text <txt>
:I  <l> <txt>  - insert text at the beginning of line <l>
:A  <l> <txt>  - append text after the end of line <l>

:s <l> <w> <txt> - search/replace word or regex <w> in buffer or on line <l>

:f <l>    - flood-fill entire buffer or line <l>
:fi <l>   - indent entire buffer or line <l>
:fd <l>   - de-indent entire buffer or line <l>

  Legend:
  <l> - line numbers, or range lstart:lend, e.g. '3:7'.
  <w> - one word or several enclosed in quotes.
  <txt> - longer string, typically also enclosed in quotes.
{w------------------------------------------------------------------------------
"""

class CommandParseError(Exception):
    pass

class CmdLineEditor(Command):
   """
   Base for the line editor command.
   Line editor commands catch everything, so there can be only one at a time.
   The base command does nothing except add to the buffer.
   It has no commands defined to allow the user to save or escape the editor or otherwise do anything.
   """
   key = syscmdkeys.CMD_NOMATCH
   aliases = [ syscmdkeys.CMD_NOINPUT ]
   locks = "cmd:all()"
   help_entry = 'Line Editor'
   auto_help = False

   # This command must be instanciated, and this variable must be set, before passing it into a cmdset!
   editor = None

   def parse(self):
       """
       This routine pre-parses the line to determine if it's a command, setting the following variables:
         editor_cmdstring - If this value is not 'None', then this is an editor command.
         editor_switches  - If editor_cmdstring is not 'None', then this should contain a list of switches passed to the command
         editor_args      - if editor_cmdstring is not 'None', then this should contain a list of arguments passed to the command
         editor_inputline - If this value is not 'None', then this is a line of freeform input from the user.  Typically this is appended to the buffer.
       If editor_cmdstring and editor_inputline are 'None' then in indicates a parsing error, and the func() call should simply return.  This routine will take care of alerting the user if needed.
       """
       self.editor_cmdstring = None
       self.editor_switches = None
       self.editor_args = None
       self.editor_inputline = self.raw_string

   def func():
       self.editor.insert(self.raw_string)


class CmdLineEditorVi(Command):
   """
   Commands for the editor (vi Style)
   """
   key = syscmdkeys.CMD_NOMATCH
   aliases = [ syscmdkeys.CMD_NOINPUT ]
   locks = "cmd:all()"
   help_entry = 'Line Editor'
   auto_help = False

   # This command must be instanciated, and this variable must be set, before passing it into a cmdset!
   editor = None

   def parse(self):
       # Set default values
       self.editor_inputline = None
       self.editor_cmdstring = None
       self.editor_switches = None
       self.editor_args = None
       self.editor_vi_lstart = None
       self.editor_vi_lend = None
       # Check if we're dealing with a command, or with input
       if self.raw_string.startswith(':'):
           try:
               # Split the command from the arguments, then split the arguments
               cmd_and_args = self.raw_string.split(' ', 1)
               self.editor_cmdstring = cmd_and_args[0]
               if len(cmd_and_args) > 1:
                   try:
                       self.editor_args = shlex.split(cmd_and_args[1])
                   except ValueError, e:
                       raise CommandParseError(str(e))
               else:
                   self.editor_args = []
               # Parse line number(s), if supplied
               if len(self.editor_args) > 0:
                   lines_match = re.search(r'^(\d+)(:(\d+))?$', self.editor_args[0])
                   if lines_match: # Only set lstart and lend if it matches the pattern.  Otherwise leave it 'None'
                       self.editor_vi_lstart = int(lines_match.group(1))
                       if lines_match.group(3):
                           self.editor_vi_lend = int(lines_match.group(3))
                       else:
                           self.editor_vi_lend = self.editor_vi_lstart
                       self.editor_args.pop(0)
               # Set unused values to None
               self.editor_switches = None
           except CommandParseError, e:
               self.caller.msg('{rCould not parse command: ' + str(e))
               # Clear any values that may have been set before the parse error, for safety
               self.editor_cmdstring = None
               self.editor_switches = None
               self.editor_args = None
               self.editor_vi_lstart = None
               self.editor_vi_lend = None
       else:
           self.editor_inputline = self.raw_string

   def func(self):
       if self.editor_cmdstring != None:
           if self.editor_cmdstring == ':':
               if self.editor_args:
                   self.caller.msg('{rThe ":" command takes no arguments.')
                   return
               self.editor.display_buffer(start=self.editor_vi_lstart, end=self.editor_vi_lend, raw=False)
           elif self.editor_cmdstring == '::':
               if self.editor_args:
                   self.caller.msg('{rThe "::" command takes no arguments.')
                   return
               self.editor.display_buffer(start=self.editor_vi_lstart, end=self.editor_vi_lend, raw=True)
           elif self.editor_cmdstring == ':::':
               if self.editor_args:
                   self.caller.msg('{rThe ":::" command takes no arguments.')
                   return
               self.editor.insert(':')
               self.caller.msg('Added a ":" line.')
           elif self.editor_cmdstring == ':u':
               if self.editor_args:
                   self.caller.msg('{rThe ":u" command takes no arguments.')
                   return
               self.editor.undo()
           elif self.editor_cmdstring == ':uu':
               if self.editor_args:
                   self.caller.msg('{rThe ":uu" command takes no arguments.')
                   return
               self.editor.redo()
           elif self.editor_cmdstring == ':UU':
               if self.editor_args:
                   self.caller.msg('{rThe ":UU" command takes no arguments.')
                   return
               self.editor.undo_all()
           elif self.editor_cmdstring == ':dd':
               if len(self.editor_args) != 0 or not isinstance(self.editor_vi_lstart, (int, long)) or not isinstance(self.editor_vi_lend, (int, long)):
                   self.caller.msg('{rUsage: :dd lstart[:lend]')
                   return
               self.editor.delete(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':dw':
               if not self.editor_args:
                   self.caller.msg('{rUsage: :dw [lstart[:lend]] "deleteme"')
                   return
               self.editor.sub(' '.join(self.editor_args), '', start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':DD':
               if self.editor_args:
                   self.caller.msg('{rThe ":DD" command takes no arguments.')
                   return
               self.editor.delete()
           elif self.editor_cmdstring == ':y':
               if len(self.editor_args) != 0 or not isinstance(self.editor_vi_lstart, (int, long)) or not isinstance(self.editor_vi_lend, (int, long)):
                   self.caller.msg('{rUsage: :y lstart[:lend]')
                   return
               self.editor.copy(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':x':
               if len(self.editor_args) != 0 or not isinstance(self.editor_vi_lstart, (int, long)) or not isinstance(self.editor_vi_lend, (int, long)):
                   self.caller.msg('{rUsage: :x lstart[:lend]')
                   return
               self.editor.cut(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':p':
               self.editor.paste(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':i':
               if not self.editor_args:
                   self.caller.msg('{rUsage: :dw [lstart[:lend]] "addme"')
                   return
               self.editor.insert(' '.join(self.editor_args), before_line=self.editor_vi_lstart)
           elif self.editor_cmdstring == ':r':
               self.editor.replace(' '.join(self.editor_args), line=self.editor_vi_lstart)
           elif self.editor_cmdstring == ':I':
               self.editor.prepend(string_to_prepend=' '.join(self.editor_args), line=self.editor_vi_lstart)
           elif self.editor_cmdstring == ':A':
               self.editor.append(string_to_append=' '.join(self.editor_args), line=self.editor_vi_lstart)
           elif self.editor_cmdstring == ':s':
               self.editor.sub(self.editor_args[0], ' '.join(self.editor_args), start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':f':
               self.editor.fill(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':fi':
               if len(self.editor_args) > 0 or (self.editor_vi_lstart != None and not isinstance(self.editor_vi_lstart, (int, long))) or (self.editor_vi_lstart != None and not isinstance(self.editor_vi_lend, (int, long))):
                   self.caller.msg('{rUsage: :fi lstart[:lend]')
                   return
               self.editor.indent(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':fd':
               if len(self.editor_args) > 0 or (self.editor_vi_lstart != None and not isinstance(self.editor_vi_lstart, (int, long))) or (self.editor_vi_lstart != None and not isinstance(self.editor_vi_lend, (int, long))):
                   self.caller.msg('{rUsage: :fd [lstart[:lend]]')
                   return
               self.editor.dedent(start=self.editor_vi_lstart, end=self.editor_vi_lend)
           elif self.editor_cmdstring == ':w':
               self.caller.msg('{rError saving buffer: No child class, or ":w" call not overriden by child class.')
           elif self.editor_cmdstring == ':wq':
               self.caller.msg('{rError saving buffer: No child class, or ":wq" call not overriden by child class.')
           elif self.editor_cmdstring == ':q':
               self.caller.msg('{rError quitting editor (Try reconnecting): No child class, or ":q" call not overriden by child class.')
           elif self.editor_cmdstring == ':q!':
               self.caller.msg('{rError quitting editor (Try reconnecting): No child class, or ":q!" call not overriden by child class.')
           elif self.editor_cmdstring == ':h':
               self.caller.msg(VI_HELP_STRING)
           else:
               self.caller.msg('{rUnrecognized editor command "%s".  Try ":h" for help.' % self.editor_cmdstring)
       else:
           self.editor.insert(self.raw_string)

class LineEditor(object):
    """
    This defines a line editor object.  It maintains a line buffer, and defines operations that users can perform on the buffer.
    """

    def __init__(self, caller, maxlines=None, maxwords=None, maxchars=None, color=False, key=""):
        """
        caller - who is using the editor
        key = an optional key for naming this session (such as which attribute is being edited)
        maxlines - Maximum number of lines for the user to enter (advisory)
        maxwords - Maximum number of words for the user to enter (advisory)
        maxchars - Maximum number of characters for the user to enter (advisory)
        color - Permit color codes  (If False, then get_buffer will default to returning escaped color codes)
        """
        self.caller = caller
        self.maxlines = maxlines
        self.maxwords = maxwords
        self.maxchars = maxchars
        self.color = color
        self.key = key
        self.text_buffer = []

        # store the original version
        self.pristine_buffer = []

        # undo operation buffer
        self.undo_buffer = [self.text_buffer]
        self.undo_pos = 0
        self.undo_max = 20

        # copy buffer
        self.copy_buffer = []

    def get_buffer(self, escape_colors=None):
        if escape_colors == None:
            if self.color:
                escape_colors=False
            else:
                escape_colors=True
        if escape_colors:
            return '\n'.join(self.text_buffer).replace('%', '%%').replace('{', '{{')
        else:
            return '\n'.join(self.text_buffer)

    def set_buffer(self, buf):
        if buf == None or buf == '':
            self.text_bufer = []
        else:
            self.text_buffer = buf.split('\n')
        self.pristine_buffer = list(self.text_buffer)

    def set_pristine(self):
        self.pristine_buffer = list(self.text_buffer)

    def set_color(self, color):
        self.color = color

    def set_maxlines(self, maxlines):
        self.maxlines = maxlines

    def set_maxwords(self, maxwords):
        self.maxwords = maxwords

    def set_maxchars(self, maxchars):
        self.maxchars = maxchars

    def set_key(self, key):
        self.key = key

    def is_unchanged(self):
        return self.text_buffer == self.pristine_buffer

    def display_buffer(self, start=None, end=None, raw=False):
       if raw:
           self.caller.msg(self.get_buffer())
           return
       # Generate a title string
       title = '{CText Editor'
       if self.key:
           title += ' {C[{c%s{C]' % self.key
       title = evennia_color.evennia_color_trunc_dots(title, 78)
       # Generate a footer statistic string
       nlines = len(self.text_buffer)
       if self.maxlines and nlines > self.maxlines:
           slines = '{r%d{C/%d' % (nlines, self.maxlines)
       elif self.maxlines:
           slines = '{C%d/%d' % (nlines, self.maxlines)
       else:
           slines = '{C%d' % (nlines)
       nwords = len([ word for word in re.split(r'\s+', '\n'.join(self.text_buffer)) if word != ''])
       if self.maxwords and nwords > self.maxwords:
           swords = '{r%d{C/%d' % (nwords, self.maxwords)
       elif self.maxwords:
           swords = '{C%d/%d' % (nwords, self.maxwords)
       else:
           swords = '{C%d' % (nwords)
       nchars = len('\n'.join(self.text_buffer))
       if self.maxchars and nchars > self.maxchars:
           schars = '{r%d{C/%d' % (nchars, self.maxchars)
       elif self.maxchars:
           schars = '{C%d/%d' % (nchars, self.maxchars)
       else:
           schars = '{C%d' % (nchars)
       footer_info = '{C[l:%s {Cw:%s {Cc:%s{C]' % (slines, swords, schars)

       # Combine the strings into a header and footer
       header = evennia_color.EvenniaColorCanvas()
       header.evennia_import('{w------------------------------------------------------------------------------')
       header.draw_string(header.width() / 2 - (evennia_color.evennia_color_len(title) / 2), 0, title)
       footer = evennia_color.EvenniaColorCanvas()
       footer.evennia_import('{w---------------------------------------------------------------{b[{c:h{b for help]{w--')
       footer.draw_string(3, 0, footer_info)
       self.caller.msg(header.evennia_export())
       if self.text_buffer == []:
           self.caller.msg('      {rEmpty Buffer')
       else:
           for lineno, line in enumerate(self.text_buffer):
               if self.color:
                   self.caller.msg('{c%5s {n%s' % (lineno + 1, line))
               else:
                   self.caller.msg('{c%5s {n%s' % (lineno + 1, line.replace('%', '%%').replace('{', '{{')))
       self.caller.msg(footer.evennia_export())
        
    def undo(self):
        self.caller.msg('STUB: undo not implemented')

    def redo(self):
        self.caller.msg('STUB: redo not implemented')

    def undo_all(self):
        self.caller.msg('STUB: undo_all not implemented')

    def delete(self, start=None, end=None):
        if end and (start > len(self.text_buffer) or start < 1):
            self.caller.msg('{rNo such start line.')
            return
        if end and (end > len(self.text_buffer) or end < 1):
            self.caller.msg('{rNo such end line.')
            return
        if start != None:
            start_index = start - 1
        else:
            start_index = None
        del self.text_buffer[start_index:end]
        if start == None and end == None:
            self.caller.msg('Deleted all lines')
        elif end == None:
            self.caller.msg('Deleted all lines from %d' % (start))
        elif start == None:
            self.caller.msg('Deleted all lines up to %d' % (end))
        elif start == end:
            self.caller.msg('Deleted line %d' % (start))
        else:
            self.caller.msg('Deleted lines %d to %d' % (start, end))

    def sub(regex, replacement, start=None, end=None):
        self.caller.msg('STUB: sub not implemented')

    def copy(self, start=None, end=None):
        self.caller.msg('STUB: copy not implemented')

    def cut(self, start=None, end=None):
        self.caller.msg('STUB: cut not implemented')

    def paste(self, after_line=None):
        self.caller.msg('STUB: paste not implemented')

    def insert(self, line_string='', before_line=None):
        if before_line != None:
            if before_line > len(self.text_buffer) or before_line < 1:
                self.caller.msg('{rNo such line number.')
                return
            self.text_buffer.insert(before_line - 1, line_string)
        else:
            self.text_buffer.append(line_string)
        if before_line != None:
            self.caller.msg('Inserted line %d' % (before_line))

    def replace(self, line, line_string=''):
        self.caller.msg('STUB: replace not implemented')

    def prepend(self, line, string_to_prepend):
        self.caller.msg('STUB: prepend not implemented')

    def append(self, line, string_to_append):
        self.caller.msg('STUB: append not implemented')

    def indent(self, width=4, start=None, end=None):
        self.caller.msg('STUB: indent not implemented')

    def dedent(self, width=4, start=None, end=None):
        self.caller.msg('STUB: dedent not implemented')
