from ev import default_cmds, settings
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
        self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))

    def cmd_list(self):
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        self.msg('')
        for option in self.prefs():
            self.msg('{C%s:{n %s' % (option, str(getattr(self, 'pref_' + option)())))
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")

    def cmd_set(self, option, value):
        if not option in self.prefs():
            self.msg('{R["%s" is not a valid option]' % (option))
            return
        try:
            getattr(self, 'pref_' + option)(value)
            self.msg('{G[Preference set]')
        except PrefValueException as e:
            self.msg('{R[Could not set value: %s]' % e)
        except:
            raise

    def prefs(self):
        return [name[5:] for name, val in inspect.getmembers(self) if name.startswith('pref_')]

    def pref_auto_ic(self, newval = None):
        player = self.caller
        if newval:
            if not newval in ['yes', 'no']:
                raise PrefValueException('Value must be "yes", or "no"')
            player.db.pref_auto_ic = newval == 'yes'
            return newval
        else:
            return player.db.pref_auto_ic and 'yes' or 'no'

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

    def pref_encoding(self, newval = None):
        player = self.caller
        if newval:
            if newval not in settings.ENCODINGS:
                raise PrefValueException('Encoding "%s" not supported on this server.  (Valid values: %s)' % (newval, ', '.join(settings.ENCODINGS)))
            player.db.encoding = newval
        return player.db.encoding
