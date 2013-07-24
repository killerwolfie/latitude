from ev import default_cmds, syscmdkeys, CmdSet, create_message, utils, managers
from game.gamesrc.latitude.utils import lineeditor
import pickle

class CmdSysAnnounce(default_cmds.MuxCommand):
    """
    @announce - Send a system-wide @page mail
    """

    key = "@announce"
    aliases = []
    locks = "cmd:perm(commands_@announce) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        input_cmd = CmdAnnounceEdit()
        input_cmd.editor = lineeditor.LineEditor(self.caller, maxchars=None, maxlines=None, color=True, key='Announcement Text')
        input_cmd.editor.display_buffer()
        input_cmdset = CmdsetAnnounce()
        input_cmdset.add(input_cmd)
        self.caller.cmdset.add(input_cmdset)

class CmdsetAnnounce(CmdSet):
    key = "CmdsetAnnounce"
    priority = 33
    mergetype = "Replace"
    no_exits = True
    no_objs = True
    no_channels = True
    def at_cmdset_creation(self):
        pass

class CmdAnnounceEdit(lineeditor.CmdLineEditorVi):
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
            self.msg("{rCan't save the message without sending.  Use :wq to send.")
        elif self.editor_cmdstring == ':wq':
            if self.editor_args:
                self.msg('{rThe ":wq" command takes no arguments.')
                return
            self.send_message()
        else:
            return super(CmdAnnounceEdit, self).func() # Try the default commands

    def send_message(self):
#        utils.run_async(self.send_message_run, self)  # FIXME Upstream issue 407
        self.send_message_run()
        # We're done.  Finish up the command
        self.caller.cmdset.delete('CmdsetAnnounce')
        self.msg('{G[Message sent, editor closed]')

    def send_message_run(self):
        # Determine the sender object (Won't actually be seen in the message.  The header is used for that.)
        sender = self.caller
        if hasattr(sender, 'player'):
            sender = sender.player
        # Get the recipients
        receivers = managers.players.all()
        # Collect the message from the user
        message = self.editor.get_buffer()
        # Generate message header, to store the 'to' and 'from' as provided.  (The recievers and sender field of the Msg object will be the player, and never a character)
        header = {
            'from' : 'Latitude MUD',
            'to' : ['All Users'],
        }
        header = pickle.dumps(header)
        # Create the message object
        msg_object = create_message(sender, message, receivers=receivers, header=header)
        # Mark the message as 'unseen' so it can be read later if desired
        for receiver in receivers:
            if not receiver.db.msg_unseen:
                receiver.db.msg_unseen = []
            receiver.db.msg_unseen.append(msg_object)
        for receiver in receivers:
            receiver.msg("{Y[You've received a page mail.  Use \"{y@page{Y\" to view it]")

    def cancel(self):
        self.caller.cmdset.delete('CmdsetAnnounce')
        self.msg('{Y[Message not sent, editor closed]')
