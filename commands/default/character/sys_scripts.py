from ev import default_cmds

class CmdSysScripts(default_cmds.CmdScripts):
    """
    Operate and list global scripts, list all scrips.

    Usage:
      @scripts[/switches] [<obj or scriptid or script.path>]

    Switches:
      start - start a script (must supply a script path)
      stop - stops an existing script
      kill - kills a script - without running its cleanup hooks
      validate - run a validation on the script(s)

    If no switches are given, this command just views all active
    scripts. The argument can be either an object, at which point it
    will be searched for all scripts defined on it, or an script name
    or dbref. For using the /stop switch, a unique script dbref is
    required since whole classes of scripts often have the same name.

    Use @script for managing commands on objects.
    """
    key = "@scripts"
    aliases = []
    locks = "cmd:perm(command_@scripts) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

