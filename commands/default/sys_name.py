from ev import default_cmds

class CmdSysName(default_cmds.CmdName):
    """
    cname - change the name and/or aliases of an object

    Usage:
      @name obj = name;alias1;alias2

    Rename an object to something new.

    """

    key = "@name"
    aliases = ["@rename"]
    locks = "cmd:pperm(rename) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

