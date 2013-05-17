from ev import default_cmds

class CmdSysOpen(default_cmds.CmdOpen):
    """
    @open - create new exit

    Usage:
      @open <new exit>[;alias;alias..][:typeclass] [,<return exit>[;alias;..][:typeclass]]] = <destination>

    Handles the creation of exits. If a destination is given, the exit
    will point there. The <return exit> argument sets up an exit at the
    destination leading back to the current room. Destination name
    can be given both as a #dbref and a name, if that name is globally
    unique.

    """
    key = "@open"
    locks = "cmd:pperm(command_@open) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
