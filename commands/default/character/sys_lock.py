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
       'get: id(25) or pperm(Janitors)'
    The 'get' access_type is checked by the get command and will
    an object locked with this string will only be possible to
    pick up by Wizards or by object with id 25.

    You can add several access_types after oneanother by separating
    them by ';', i.e:
       'get:id(25);delete:pperm(Custodians)'
    """
    key = "@lock"
    aliases = []
    locks = "cmd: pperm(@locks) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
