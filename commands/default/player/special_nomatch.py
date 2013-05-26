from ev import Command
from ev import syscmdkeys
import random

class CmdNoMatch(Command):
    key = syscmdkeys.CMD_NOMATCH
    locks = "cmd:all()"
    auto_help = False

    def func(self):
        cmdline = self.args
        cmd = cmdline.split()[0]
        caller = self.caller
        sessid = self.sessid
        # Check if we're OOC, or if we're explicitly typing a system command with @cmd, in which case, just tell them it's an invalid command.
        if cmd[0] == '@' or not hasattr(caller, 'player'):
            self.msg('"%s" command not found.  (Try "help" for a list of commands)' % cmd)
            return
        # Check for a direction match
        for direction in [
            ('north', 'north'),
            ('south', 'south'),
            ('east', 'east'),
            ('west', 'west'),
            ('up', 'up'),
            ('down', 'down'),
            ('in', 'in'),
            ('out', 'out'),
            ('northeast', 'northeast'),
            ('northwest', 'northwest'),
            ('southeast', 'southeast'),
            ('southwest', 'southwest'),
            ('ne', 'northeast'),
            ('nw', 'northwest'),
            ('se', 'southeast'),
            ('sw', 'southwest'),
        ]:
            if direction[0].startswith(cmdline.lower()):
                self.msg("You can't go %s from here." % direction[1])
                return
        # Unknown action.
        self.msg('You try to "%s" but it doesn\'t seem to work here.' % cmd)
