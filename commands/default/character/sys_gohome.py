from src.commands.default import general

class CmdSysGoHome(general.CmdHome):
    """
    home

    Usage:
      @gohome

    Teleports you to your home location.
    """

    key = "@gohome"
    locks = "cmd:perm(command_@gohome) or perm(Janitors)"
    help_category = "--- Coder/Sysadmin ---"
