from ev import default_cmds

class CmdSysCmdSets(default_cmds.CmdListCmdSets):
    """
    list command sets on an object

    Usage:
      @cmdsets [obj]

    This displays all cmdsets assigned
    to a user. Defaults to yourself.
    """
    key = "@cmdsets"
    aliases = "@listcmsets"
    locks = "cmd:pperm(command_@cmdsets) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

