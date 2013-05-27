from ev import default_cmds

class CmdSysCWho(default_cmds.CmdCWho):
    """
    @cwho

    Usage:
      @cwho <channel>

    List who is connected to a given channel you have access to.
    """
    key = "@cwho"
    locks = "cmd:perm(command_@cwho) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

