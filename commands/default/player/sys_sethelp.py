from ev import CmdSet, syscmdkeys, search_help_entry, create_help_entry
from game.gamesrc.latitude.utils import lineeditor
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysSetHelp(LatitudeCommand):
    """
    @sethelp - edit the help database

    Usage:
      @sethelp <topic>
        Edits the text of a given help topic.

      @sethelp/category <topic>=<category>
        Sets the category of a given help topic.

      @sethelp/locks <topic>=<lockstring>
        Sets the lock string for a given help topic.

      @sethelp/delete <topic>
        Removes a given help topic.
    """
    key = "@sethelp"
    aliases = []
    locks = "cmd:perm(command_@sethelp) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"
    logged = True

    def func(self):
        if not self.switches and self.args:
            self.cmd_edit(self.args)
        elif self.switches == [ 'category' ] and self.lhs and self.rhs:
            self.cmd_category(self.lhs, self.rhs)
        elif self.switches == [ 'locks' ] and self.lhs and self.rhs:
            self.cmd_locks(self.lhs, self.rhs)
        elif self.switches == [ 'delete' ] and self.args:
            self.cmd_delete(self.args)
        else:
            # Unrecognized command
            self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))

    def cmd_edit(self, topic):
        help_entry = search_help_entry(topic)
        if help_entry:
            help_entry = help_entry[0]
        else:
            help_entry = None
        input_cmd = CmdSetHelpEdit()
        input_cmd.editor = lineeditor.LineEditor(self.caller, maxchars=None, maxlines=None, color=True, key='Help: ' + topic)
        if help_entry:
            input_cmd.editor.set_buffer(help_entry.entrytext)
        input_cmd.editor.display_buffer()
        input_cmd.help_topic = topic
        input_cmd.help_entry = help_entry
        input_cmdset = CmdsetSetHelp()
        input_cmdset.add(input_cmd)
        self.caller.cmdset.add(input_cmdset)

    def cmd_category(self, topic, category):
        help_entry = search_help_entry(topic)
        if help_entry:
            help_entry = help_entry[0]
        else:
            self.msg('{R[Topic not found]')
            return
        help_entry.help_category = category
        self.msg('{G[Category set]')

    def cmd_locks(self, topic, lockstring):
        help_entry = search_help_entry(topic)
        if help_entry:
            help_entry = help_entry[0]
        else:
            self.msg('{R[Topic not found]')
            return
        help_entry.locks.clear()
        if help_entry.locks.add(lockstring):
            self.msg('{G[Lock string set]')
        else:
            self.msg('{R[Failed to set lock string (Invalid string?)]') # FIXME: Upstream issue 410

    def cmd_delete(self, topic):
        help_entry = search_help_entry(topic)
        if help_entry:
            help_entry = help_entry[0]
        else:
            self.msg('{R[Topic not found]')
            return
        help_entry.delete()
        self.msg('{G[Topic deleted]')

class CmdsetSetHelp(CmdSet):
    key = "CmdsetSetHelp"
    priority = 33
    mergetype = "Replace"
    no_exits = True
    no_objs = True
    no_channels = True
    def at_cmdset_creation(self):
        pass

class CmdSetHelpEdit(lineeditor.CmdLineEditorVi):
    key = syscmdkeys.CMD_NOMATCH
    aliases = [ syscmdkeys.CMD_NOINPUT ]
    locks = "cmd:all()"

    def func(self):
        # We're currently inside a field.  So pass commands to the editor.
        if self.editor_cmdstring == ':q':
            if self.editor_args:
                self.msg('{rThe ":q" command takes no arguments.')
                return
            if not self.editor.is_unchanged():
                self.msg('{rText has changed.  Use ":wq" to send, or ":q!" to quit.')
                return
            self.cancel()
        elif self.editor_cmdstring == ':q!':
            if self.editor_args:
                self.msg('{rThe ":q!" command takes no arguments.')
                return
            self.cancel()
        elif self.editor_cmdstring == ':w':
            if self.editor_args:
                self.msg('{rThe ":w" command takes no arguments.')
                return
            self.set_help(close=False)
        elif self.editor_cmdstring == ':wq':
            if self.editor_args:
                self.msg('{rThe ":wq" command takes no arguments.')
                return
            self.set_help(close=True)
        else:
            return super(CmdSetHelpEdit, self).func() # Try the default commands

    def set_help(self, close=False):
        if self.help_entry:
            self.help_entry.entrytext = self.editor.get_buffer()
        else:
            self.help_entry = create_help_entry(self.help_topic, self.editor.get_buffer())
        if close:
            # We're done.  Finish up the command
            self.caller.cmdset.delete('CmdsetSetHelp')
            self.msg('{G[Help entry set, editor closed]')
        else:
            self.msg('{G[Help entry set]')

    def cancel(self):
        self.caller.cmdset.delete('CmdsetSetHelp')
        self.msg('{Y[Cancelled, editor closed]')
