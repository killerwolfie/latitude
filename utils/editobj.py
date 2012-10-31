"""
"""

from ev import Command, CmdSet, syscmdkeys, Character, Player, search_object, search_player
from game.gamesrc.latitude.utils import lineeditor
from game.gamesrc.latitude.utils.evennia_color import evennia_color_left, evennia_color_len, EvenniaColorCanvas
import unicodedata, re

##############################################################################
# Configuration
##############################################################################
UNIQUE_CHARACTER_NAMES = True
UNIQUE_PLAYER_NAMES = True

# Some hard coded defaults, overridable by the field definitions
DEFAULTS = {
    'NAME' : {
        'cols' : 1,
        'color' : False,
        'maxchars' : 30,
        'maxwords' : None,
        'maxlines' : 1,
        'invalid_regex' : re.compile(r'[^\w \.]'),
    },
    'ATTR' : {
        'cols' : 1,
        'color' : False,
        'maxchars' : 10000,
        'maxwords' : None,
        'maxlines' : 100,
        'invalid_regex' : re.compile(r'[\x00-\x09\x0B-\x1F\x80-\x9F]'),
    },
    'SEP' : {
        'cols' : 1,
        'menutext' : None,
    }
}

# TODO: Define a list of required attributes, and valid attributes and check at __init__ time

##############################################################################
# Class Definitions
##############################################################################
class CmdEditObj(lineeditor.CmdLineEditorVi):
    """
    This command catches all unmatched input and passes it to the object editor.
    """
    key = syscmdkeys.CMD_NOMATCH
    aliases = [ syscmdkeys.CMD_NOINPUT ]
    locks = "cmd:all()"

    def func(self):
       if self.objedit.state_current_field:
           # We're currently inside a field.  So pass commands to the editor.
           if self.editor_cmdstring != None:
               if self.editor_cmdstring == ':q':
                   if self.editor_args:
                       self.caller.msg('{rThe ":q" command takes no arguments.')
                       return
                   if not self.editor.is_unchanged():
                       self.caller.msg('{rText has changed.  Use ":w" to save changes before quitting.')
                       return
                   self.objedit.close_field()
               elif self.editor_cmdstring == ':q!':
                   if self.editor_args:
                       self.caller.msg('{rThe ":q!" command takes no arguments.')
                       return
                   self.objedit.close_field()
               elif self.editor_cmdstring == ':w':
                   if self.editor_args:
                       self.caller.msg('{rThe ":w" command takes no arguments.')
                       return
                   self.objedit.save_field(close=False)
               elif self.editor_cmdstring == ':wq':
                   if self.editor_args:
                       self.caller.msg('{rThe ":wq" command takes no arguments.')
                       return
                   self.objedit.save_field(close=True)
               else:
                   return super(CmdEditObj, self).func() # Try the default commands
           else:
               return super(CmdEditObj, self).func() # No command, use default behavior.
       elif self.objedit.state_asking_to_save:
           if self.raw_string.lower() == 'y':
               if self.objedit.commit_precheck():
                   self.objedit.commit()
                   self.objedit.quit()
               else:
                   self.caller.msg('Do you still want to try committing your changes?  [Y/N/C]:')
           elif self.raw_string.lower() == 'n':
               self.objedit.quit()
           elif self.raw_string.lower() == 'c':
               self.objedit.state_asking_to_save = False
               self.objedit.display_menu()
           else:
               self.caller.msg('Please use "Y", "N", or "C" to make your selection.  Do you want to commit your changes?  [Y/N/C]:')
       else:
           # Catch requests to quit
           if self.args.lower() == 'q':
               self.caller.msg('Do you want to commit your changes?  [Y/N/C]:')
               self.objedit.state_asking_to_save = True
               return
           
           # We're not in the editor, so process commands for the menu
           self.objedit.open_field(self.args)

class CmdsetEditObj(CmdSet):
    """
    A CmdSet which is completely empty except for a single CMD_NOMATCH command, so that all input from the user is interpreted by the ObjEdit class.
    The CMD_NOMATCH command needs to be added to the object after creation, because the ObjEdit class modifies it slightly from a basic instance
    (Specifically, it imbuse the command with a reference to the ObjEdit class itself)
    """
    key = "ObjEdit"
    priority = 11
    mergetype = "Replace"
    no_exits = True
    no_objs = True
    no_channels = True
    def at_cmdset_creation(self):
        pass

class EditObj(object):
    """
    This class puts a ObjEditCmdset onto the user which overrides all commands and interprets all input, and passes it off to appropriate editor command classes.
    It also acts as a data store for the current state of the menu as the user navigates through it.
    """
    def __init__(self, caller, obj, fields, confirm=True, key='Editor'):
        # Store settings
        self.caller = caller
        self.obj = obj.typeclass # 'isinstance' is used, requiring typeclass, not DB classes
        self.fields = list(fields)
        self.confirm = confirm
        self.key = key
        # Initialize state
        self.state_current_field = None
        self.state_asking_to_save = False
        self.edited_attr = {}
        self.edited_name = None
        # Create an editor object to contain a text buffer to be used as needed
        self.editor = lineeditor.LineEditor(caller, maxchars=10, maxlines=3, color=True, key='')
        # Validate fields and add defaults if needed
        for field in self.fields:
            if field['type'] in DEFAULTS:
                for def_attr, def_val in DEFAULTS[field['type']].items():
                    if not def_attr in field:
                        field[def_attr] = def_val
        caller.msg(self.fields, data={'raw' : True})
        # Create and attach the editor cmdset to the user
        cmdset = CmdsetEditObj()
        cmd_entry = CmdEditObj()
        cmd_entry.objedit = self
        cmd_entry.editor = self.editor
        cmdset.add(cmd_entry)
        if hasattr(caller, 'player'):
            caller.player.cmdset.add(cmdset)
        caller.cmdset.add(cmdset)
        self.display_menu()

    def display_menu(self):
        menu_string = ''
        # Render header
        header = EvenniaColorCanvas()
        header.evennia_import('{w------------------------------------------------------------------------------')
        header.draw_string(5, 0, '{B[{y %s {B]' % (self.key))
        item_string = '{B[{c %s {B]' % (self.obj.key)
        header.draw_string(73 - evennia_color_len(item_string), 0, item_string)
        menu_string += header.evennia_export() + '\n\n'
        # Render body
        current_max_columns = None
        current_column = 1
        for field in self.fields:
            need_new_line = False
            if current_max_columns != None: # We're not at the beginning.  Check if we need a newline.
                if current_column >= current_max_columns:
                    need_new_line = True
                    current_column = 1
                else:
                    current_column += 1
            # If the number of columns per row changes, add a newline, and reset the current number of columns
            if field['cols'] != current_max_columns:
                if current_max_columns != None:
                    need_new_line = True
                current_max_columns = field['cols']
            # Apply a newline if needed
            if need_new_line:
                menu_string += '\n'
            # Add this field to the list
            if field['type'] == 'NAME':
                if self.edited_name:
                    name_string = self.edited_name
                else:
                    name_string = self.obj.key
                menu_string += evennia_color_left('{C%s {b%s' % (field['menutext'], name_string), 78 / current_max_columns, dots=True)
            elif field['type'] == 'ATTR':
                if self.obj.has_attribute(field['attribute']):
                    if field['attribute'] in self.edited_attr:
                        attr_string = self.edited_attr[field['attribute']]
                    else:
                        attr_string = self.obj.get_attribute(field['attribute'])
                    if '\n' in attr_string:
                       attr_string = attr_string.split('\n')[0]
                       attr_string += '...'
                else:
                    attr_string = '{B[Unset]'
                menu_string += evennia_color_left('{C%s {b%s' % (field['menutext'], attr_string), 78 / current_max_columns, dots=True)
            elif field['type'] == 'SEP':
                separator = EvenniaColorCanvas()
                separator.evennia_import('{w------------------------------------------------------------------------------')
                sep_desc = '{B[{C %s {B]' % (field['menutext'])
                separator.draw_string(5, 0, sep_desc)
                menu_string += '\n' + separator.evennia_export()
            else:
                raise(Exception('Invalid field type in EditObj class'))
        # Render footer
        menu_string += '\n\n{w------------------------------------------------------------------------------'
        menu_string += "\n{nPlease make a selection, or enter 'Q' to quit.  (You'll be prompted to save.)"
        # Print result
        self.caller.msg(menu_string)

    def open_field(self, key):
        for field in self.fields:
            if 'key' in field and field['key'].lower() == key.lower():
                # Handle 'text editor' type fields
                if field['type'] == 'ATTR' or field['type'] == 'NAME':
                    self.editor.set_color(field['color'])
                    self.editor.set_maxchars(field['maxchars'])
                    self.editor.set_maxwords(field['maxwords'])
                    self.editor.set_maxlines(field['maxlines'])
                    self.editor.set_key(field['desc'])
                    if field['type'] == 'ATTR':
                        if field['attribute'] in self.edited_attr:
                            self.editor.set_buffer(self.edited_attr[field['attribute']])
                        elif self.obj.has_attribute(field['attribute']):
                            self.editor.set_buffer(self.obj.get_attribute(field['attribute']))
                        else:
                            self.editor.set_buffer(None)
                    elif field['type'] == 'NAME':
                        if self.edited_name:
                            self.editor.set_buffer(self.edited_name)
                        else:
                            self.editor.set_buffer(self.obj.key)
                else:
                    continue
                self.state_current_field = field
                self.caller.msg('\nNow editing "%s"...' % field['desc'])
                self.editor.display_buffer()
                return
        self.caller.msg('{rThat seems to be an invalid menu selection.')

    def save_field(self, close=False):
        # Process the buffer, if this field is a line editor type
        if self.state_current_field['type'] == 'ATTR' or self.state_current_field['type'] == 'NAME':
            # Verify that they supplied kosher results
            new_val = self.editor.get_buffer()
            if self.state_current_field['maxchars'] != None and len(new_val) > self.state_current_field['maxchars']:
                self.caller.msg('{rUnable to save: Too many characters')
                return
            if self.state_current_field['maxwords'] != None and len([ word for word in re.split(r'\s+', new_val) if word != '']) > self.state_current_field['maxwords']:
                self.caller.msg('{rUnable to save: Too many words')
                return
            if self.state_current_field['maxlines'] != None and len(new_val.split('\n')) > self.state_current_field['maxlines']:
                self.caller.msg('{rUnable to save: Too many lines')
                return
            if self.state_current_field['invalid_regex'] != None and re.search(self.state_current_field['invalid_regex'], new_val):
                self.caller.msg('{rUnable to save: Invalid characters detected.')
                return
            if self.state_current_field['type'] == 'NAME' and not new_val:
                self.caller.msg("{rNames can't be blank")
                return
            if UNIQUE_CHARACTER_NAMES and self.state_current_field['type'] == 'NAME' and isinstance(self.obj, Character):
                if new_val != self.obj.name: # Pass if they're trying to change the name of the object to what it already is
                    if [obj for obj in search_object(new_val) if isinstance(obj, Character)]:
                        self.caller.msg('{rThat name is already taken.')
                        return
                    if new_val != self.obj.player.name and search_player(new_val):
                        self.caller.msg("{rThat name matches someone's login.")
                        return
            if UNIQUE_PLAYER_NAMES and self.state_current_field['type'] == 'NAME' and isinstance(self.obj, Player):
                if new_val != self.obj.name: # Pass if they're trying to change the name of the object to what it already is
                    if search_player(new_val):
                        self.caller.msg('{rThat name is already taken.')
                        return
                    if new_val != self.obj.character.name and [obj for obj in search_object(new_val) if isinstance(obj, Character)]:
                        self.caller.msg("{rThat name matches the name of someone's character.")
                        return
            # Perform the save
            if self.state_current_field['type'] == 'ATTR':
                self.edited_attr[self.state_current_field['attribute']] = new_val
            elif self.state_current_field['type'] == 'NAME':
                self.edited_name = new_val
            # Set the buffer pristine (Matching what's saved)
            self.editor.set_pristine()
        # Alert the user that we've complete (Should have bailed by now if there were errors)
        self.caller.msg('{GCurrent buffer saved.  Use "Q" on the main menu commit the change to the object.')
        # Close if requested
        if close:
            self.close_field()

    def close_field(self):
        self.state_current_field = None
        self.caller.msg('... Editor closed.')
        self.display_menu()

    def commit_precheck(self):
        # Do some last minute safety checks
        if UNIQUE_CHARACTER_NAMES and self.edited_name and isinstance(self.obj, Character):
            if self.edited_name != self.obj.name: # Pass if they're trying to change the name of the object to what it already is
                if [obj for obj in search_object(self.edited_name) if isinstance(obj, Character)]:
                    self.caller.msg('{rCould not commit changes: Character name already taken.')
                    return False
                if self.edited_name != self.obj.player.name and search_player(self.edited_name):
                    self.caller.msg("{rCould not commit changes: Character name already assigned to player.")
                    return False
        if UNIQUE_PLAYER_NAMES and self.edited_name and isinstance(self.obj, Player):
            if self.edited_name != self.obj.name: # Pass if they're trying to change the name of the object to what it already is
                if search_player(self.edited_name):
                    self.caller.msg('{rCould not commit changes: Player name is already taken.')
                    return False
                if self.edited_name != self.obj.character.name and [obj for obj in search_object(self.edited_name) if isinstance(obj, Character)]:
                    self.caller.msg("{rCould not commit changes: Player name is already assigned to character.")
                    return False
        return True

    def commit(self):
        if self.edited_name:
            self.obj.name = self.edited_name
        for attr_name, attr_val in self.edited_attr.items():
            self.obj.set_attribute(attr_name, attr_val)
        self.caller.msg('{gChanges committed.')

    def quit(self):
        if hasattr(self.caller, 'player'):
            self.caller.player.cmdset.delete('ObjEdit')
        self.caller.cmdset.delete('ObjEdit')
        self.caller.execute_cmd('look')

class CmdEditTest(Command):
    """
    edit testing command

    Usage:
        edit
    """
    key = "edit"
    locks = "cmd:all()"
    help_category = "Testing"

    def func(self):
        "Testing the edit system"
        EditObj(caller=self.caller, obj=self.caller, key='Editor Test', fields=[
            {
                'key'  : '1',
                'type' : 'NAME',
                'menutext' : '{C[{c1{C] Name:   ',
                'desc' : 'Name',
                'cols' : 2,
            },
            {
                'key' : '2',
                'type' : 'ATTR',
                'menutext' : '{C[{c2{C] Gender: ',
                'desc' : 'Gender',
                'attribute' : 'attr_gender',
                'cols' : 2,
                'maxchars' : 10,
                'maxwords' : 1,
            },
            {
                'type' : 'SEP',
                'menutext' : 'Descriptions',
                'cols' : 1,
            },
            {
                'key' : 'D1',
                'type' : 'ATTR',
                'menutext' : '{C[{cD1{C] Appearance: ',
                'desc' : 'Appearance',
                'attribute' : 'desc_appearance',
                'cols' : 1,
            },
            {
                'key' : 'D2',
                'type' : 'ATTR',
                'menutext' : '{C[{cD2{C] Scent:      ',
                'desc' : 'Scent',
                'attribute' : 'desc_scent',
                'cols' : 1,
            },
            {
                'key' : 'D3',
                'type' : 'ATTR',
                'menutext' : '{C[{cD3{C] Texture:    ',
                'desc' : 'Texture',
                'attribute' : 'desc_texture',
                'cols' : 1,
            },
            {
                'key' : 'D4',
                'type' : 'ATTR',
                'menutext' : '{C[{cD4{C] Flavor:     ',
                'desc' : 'Flavor',
                'attribute' : 'desc_flavor',
                'cols' : 1,
            },
            {
                'key' : 'D5',
                'type' : 'ATTR',
                'menutext' : '{C[{cD5{C] Aura:       ',
                'desc' : 'Aura',
                'attribute' : 'desc_aura',
                'cols' : 1,
            },
            {
                'key' : 'D6',
                'type' : 'ATTR',
                'menutext' : '{C[{cD6{C] Sound:      ',
                'desc' : 'Sound',
                'attribute' : 'desc_sound',
                'cols' : 1,
            },
            {
                'key' : 'D7',
                'type' : 'ATTR',
                'menutext' : '{C[{cD7{C] Writing:    ',
                'desc' : 'Writing',
                'attribute' : 'desc_writing',
                'cols' : 1,
            },
        ])
