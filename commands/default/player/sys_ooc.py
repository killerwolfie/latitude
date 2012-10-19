from ev import default_cmds

class CmdSysOOC(default_cmds.CmdOOC):
    """
    @ooc - go ooc

    Usage:
      @ooc

    Go out-of-character (OOC).

    This will leave your current character and put you in a incorporeal OOC state.
    """

    key = "@ooc"
    locks = "cmd:all()" # this must be all(), or different puppeted objects won't be able to access it.
    aliases = "@unpuppet"
    help_category = "General"

