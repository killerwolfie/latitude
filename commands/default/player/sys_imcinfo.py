from ev import default_cmds

class CmdSysIMCInfo(default_cmds.CmdIMCInfo):
    """
    @imcinfo - package of imc info commands

    Usage:
      @imcinfo[/switches]
      @imcchanlist - list imc2 channels
      @imclist -     list connected muds
      @imcwhois <playername> - whois info about a remote player

    Switches for @imcinfo:
      channels - as @imcchanlist (default)
      games or muds - as @imclist
      whois - as @imcwhois (requires an additional argument)
      update - force an update of all lists

    Shows lists of games or channels on the IMC2 network.
    """

    key = "@imcinfo"
    aliases = []
    locks = "cmd: serversetting(IMC2_ENABLED) and pperm(Janitors)"
    help_category = "=== Admin ==="

