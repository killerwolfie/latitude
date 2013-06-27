from game.gamesrc.latitude.scripts.script import Script
from ev import Command, CmdSet, syscmdkeys, create_script

class PromptState(Script):
    """
    Base class for a character state which requires user input.  (i.e. menus, NCP dialogs, multiple choice events, etc.)

    To use this script, create a child class, and define the methods:
        prompt_options()
            - Ouputs a list of options to self.obj
        option_<option name>
            - Handlers for each possible option selection (alphanumeric names only).
            - If the user selects an undefined option they will get an error, and prompt_options() will be called again.
            - If the return value is a script class (string or class) that is the same as the eisting class, then prompt_options() is called and no further action is taken.
            - If the return value is a script class (string or class) that is different from the existing class, then the existing class is stop()'d, and a new class with the given type is created.  (All db values are copied over)
            - If the return value is None, then the script will be stop()'d, and the prompt will end.
    """
    def at_script_creation(self):
        super(PromptState, self).at_script_creation()
        self.key = "prompt_state"
	self.interval = 0
	self.persistent = True

    def is_valid(self):
        if not self.obj:
            # Orphaned script
            return False
        if type(self) is PromptState:
            # Direct instance of base class
            return False
        return super(PromptState, self).is_valid()

    def at_start(self):
        # Construct and attach a cmdset to the object
        cmdset = PromptStateCmdset()
        cmd_entry = PromptStateCommand()
        cmd_entry.scriptobj = self
        cmdset.add(cmd_entry)
        self.obj.cmdset.add(cmdset)
        self.prompt_options()

    def at_stop(self):
        self.obj.cmdset.delete('PromptState')

    def prompt_end(self):
        """
        This handles cleanup after a user selection has been made and processed, and the prompt is over, because no script is going to take its place.

        This is called after the cmdset is removed from the character, so execute_cmd can be used safely.
        """
        self.obj.execute_cmd('look')

class PromptStateCmdset(CmdSet):
    """
    A CmdSet which is completely empty except for a single CMD_NOMATCH command, so that all input from the user is interpreted by the ObjEdit class.
    The CMD_NOMATCH command needs to be added to the object after creation, because the PromptState class modifies it slightly from a basic instance
    (Specifically, it imbuse the command with a reference to the PromptState class itself)
    """
    key = "PromptState"
    priority = 10
    mergetype = "Replace"
    key_mergetypes = {
        'Player' : 'Union',
    }
    no_exits = True
    no_objs = True
    no_channels = False
    def at_cmdset_creation(self):
        pass

class PromptStateCommand(Command):
    """
    Command class for handling user input when in a prompt state.
    It handles commands 'raw', with CMD_NOMATCH.
    """
    key = syscmdkeys.CMD_NOMATCH
    aliases = []
    locks = "cmd:all()"
    auto_help = False

    def func(self):
        # A 'scriptobj' variable is set on this command by the PromptState script when the command is constructed.
        scriptobj = self.scriptobj
        # Search the script object for a matching command
        if self.args.isalnum() and hasattr(scriptobj, 'prompt_option_' + self.args):
            newclass = getattr(scriptobj, 'prompt_option_' + self.args)()
            if newclass:
                if isinstance(newclass, basestring) and newclass == scriptobj.__module__ + '.' + scriptobj.__name__ or newclass is type(scriptobj):
                    # The class that's already in use was returned.  So just show the options again.
                    scriptobj.prompt_options()
                else:
                    # We're being replaced by a different class!  Create the new script
                    newscript = create_script(newclass, obj=scriptobj.obj, autostart=False)
                    # Copy all our attributes into the new script
                    for attr in scriptobj.get_all_attributes():
                        newscript.set_attribute(attr.key, attr.value)
                    # Stop the existing script
                    scriptobj.stop()
                    scriptobj = None
                    # Start the new one
                    newscript.start()
            else:
                # We're done, and there's nothing to replace us.
                try:
                    scriptobj.obj.cmdset.delete('PromptState') # The script at_stop will do this again for safety
                    scriptobj.prompt_end()
                except Exception:
                    raise
                finally:
                    scriptobj.stop()
                    scriptobj = None
        else:
            self.msg('{R[That selection is not recognized]')
            scriptobj.prompt_options()
