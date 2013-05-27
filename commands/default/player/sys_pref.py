from ev import default_cmds
import inspect

class PrefValueException(Exception):
    pass

class CmdSysPref(default_cmds.MuxPlayerCommand):
    """
    @pref

    Manage your player preferences.

    Usage:
      @pref
        Displays a list of options and their current values.

      @pref <name>=<value>
        Change a preference value.

    For information on individual options, see help <option name>
    """

    key = "@pref"
    locks = "cmd:all()"
    aliases = []
    help_category = "General"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        if not self.switches and not self.args:
            self.cmd_list()
            return
        elif self.lhs and self.rhs:
            self.cmd_set(self.lhs, self.rhs)
            return
        # Unrecognized command
        self.msg("Invalid '%s' command.  See 'help %s' for usage" % (self.cmdstring, self.key))

    def cmd_list(self):
        for option in self.prefs():
            self.msg('%s: %s' % (option, str(getattr(self, 'pref_' + option)())))

    def cmd_set(self, option, value):
        if not option in self.prefs():
            self.msg('{R"%s" is not a valid option.' % (option))
            return
        try:
            getattr(self, 'pref_' + option)(value)
            self.msg('Preference set.')
        except PrefValueException as e:
            self.msg('{RCould not set value: %s' % e)
        except:
            raise

    def prefs(self):
        return [name[5:] for name, val in inspect.getmembers(self) if name.startswith('pref_')]

    def pref_autofollow(self, newval = None):
        player = self.caller
        if newval:
            newval = newval.lower()
            lock_map = {
                'yes' : 'default_follow:all()',
                'no' : 'default_follow:none()',
                'friends' : 'default_follow:friend()'
            }
            if not newval in lock_map:
                raise PrefValueException('Value must be "yes", "no", or "friends"')
            player.locks.add(lock_map[newval])
            return newval
        else:
            lock_map = {
                'default_follow:all()' : 'yes',
                'default_follow:none()' : 'no',
                'default_follow:friend()' : 'friends',
                '' : 'no'
            }
            oldval = player.locks.get('default_follow')
            if oldval in lock_map:
                return lock_map[oldval]
            else:
                return 'unknown'

    def pref_autolead(self, newval = None):
        player = self.caller
        if newval:
            newval = newval.lower()
            lock_map = {
                'yes' : 'default_lead:all()',
                'no' : 'default_lead:none()',
                'friends' : 'default_lead:friend()'
            }
            if not newval in lock_map:
                raise PrefValueException('Value must be "yes", "no", or "friends"')
            player.locks.add(lock_map[newval])
            return newval
        else:
            lock_map = {
                'default_lead:all()' : 'yes',
                'default_lead:none()' : 'no',
                'default_lead:friend()' : 'friends',
                '' : 'no'
            }
            oldval = player.locks.get('default_lead')
            if oldval in lock_map:
                return lock_map[oldval]
            else:
                return 'unknown'
