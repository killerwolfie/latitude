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
    locks = "cmd:perm(command_@name) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

