from ev import default_cmds

class CmdSysLock(default_cmds.CmdLock):
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
    aliases = ["@locks", "lock", "locks"]
    locks = "cmd: perm(@locks) or perm(Builders)"
    help_category = "Building"

