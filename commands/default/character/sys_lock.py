from ev import default_cmds
from game.gamesrc.latitude.commands.muckcommand import MuckCommand

class CmdSysLock(default_cmds.CmdLock, MuckCommand):
    """
    lock - assign a lock definition to an object

    Usage:
      @lock <object>[ = <lockstring>]
      or
      @lock[/switch] object/<access_type>

    Switch:
      del - delete given access type
      view - view lock associated with given access type (default)

    If no lockstring is given, shows all locks on
    object.

    Lockstring is on the form
       'access_type:[NOT] func1(args)[ AND|OR][ NOT] func2(args) ...]
    Where func1, func2 ... valid lockfuncs with or without arguments.
    Separator expressions need not be capitalized.

    For example:
       'get: id(25) or perm(Wizards)'
    The 'get' access_type is checked by the get command and will
    an object locked with this string will only be possible to
    pick up by Wizards or by object with id 25.

    You can add several access_types after oneanother by separating
    them by ';', i.e:
       'get:id(25);delete:perm(Builders)'
    """
    key = "@lock"
    aliases = []
    locks = "cmd: pperm(command_@lock) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

    def func(self):
        "Sets up the command"

        caller = self.caller
        if not self.args:
            string = "@lock <object>[ = <lockstring>] or @lock[/switch] object/<access_type>"
            caller.msg(string)
            return
        if '/' in self.lhs:
            # call on the form @lock obj/access_type
            objname, access_type = [p.strip() for p in self.lhs.split('/', 1)]
            obj = caller.search(objname)
            if not obj:
                return
            lockdef = obj.locks.get(access_type)
            if lockdef:
                if 'del' in self.switches:
                    obj.locks.delete(access_type)
                    string = "deleted lock %s" % lockdef
            else:
                string = "%s has no lock of access type '%s'." % (obj, access_type)
            caller.msg(string)
            return

        if self.rhs:
            # we have a = separator, so we are assigning a new lock
            objname, lockdef = self.lhs, self.rhs
            obj = caller.search(objname)
            if not obj:
                return
            ok = obj.locks.add(lockdef, caller)
            if ok:
                caller.msg("Added lock '%s' to %s." % (lockdef, obj))
            return

        # if we get here, we are just viewing all locks
        obj = caller.search(self.lhs)
        if not obj:
            return
        caller.msg(obj.locks)

