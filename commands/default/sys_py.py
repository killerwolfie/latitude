from ev import default_cmds

class CmdSysPy(default_cmds.CmdPy):
    """
    Execute a snippet of python code

    Usage:
      @py <cmd>

    Separate multiple commands by ';'.  A few variables are made
    available for convenience in order to offer access to the system
    (you can import more at execution time).

    Available variables in @py environment:
      self, me                   : caller
      here                       : caller.location
      ev                         : the evennia API
      inherits_from(obj, parent) : check object inheritance

    {rNote: In the wrong hands this command is a severe security risk.
    It should only be accessible by trusted server admins/superusers.{n

    """
    key = "@py"
    aliases = ["!"]
    locks = "cmd:pperm(py) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

