from src.commands.default import general

class CmdHome(general.CmdHome):
    """
    home

    Usage:
      home

    Teleports you to your home location.
    """

    key = "home"
    locks = "cmd:perm(home) or perm(Builders)"
