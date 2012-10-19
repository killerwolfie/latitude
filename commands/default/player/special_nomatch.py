from ev import Command
from ev import syscmdkeys
import random

class CmdNoMatch(Command):
    key = syscmdkeys.CMD_NOMATCH
    locks = "cmd:all()"
    auto_help = False

    def func(self):
        command = self.args.split()[0]
        if command[0] == '@':
            self.caller.msg('"%s" command not found.  (Try "help" for a list of commands)' % command)
        else:
            self.caller.msg('You try to "%s" but it doesn\'t seem to work here.' % command)
