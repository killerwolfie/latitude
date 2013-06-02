from ev import default_cmds

class CmdSysAbout(default_cmds.CmdAbout):
    """
    @about - game engine info

    Usage:
      @about

    Display info about the game engine.
    """

    key = "@about"
    aliases = "@version"
    locks = "cmd:all()"
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

