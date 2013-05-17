from ev import default_cmds

class CmdSysAllCom(default_cmds.CmdAllCom):
    """
    @allcom - operate on all channels

    Usage:
      @allcom [on | off | who | destroy]

    Allows the user to universally turn off or on all channels they are on,
    as well as perform a 'who' for all channels they are on. Destroy deletes
    all channels that you control.

    Without argument, works like comlist.
    """

    key = "@allcom"
    locks = "cmd:pperm(command_sys_allcom) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

