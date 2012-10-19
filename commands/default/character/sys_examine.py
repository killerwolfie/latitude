from ev import default_cmds

class CmdSysExamine(default_cmds.CmdExamine):
    """
    examine - detailed info on objects

    Usage:
      examine [<object>[/attrname]]
      examine [*<player>[/attrname]]

    Switch:
      player - examine a Player (same as adding *)
      raw - don't parse escape codes for data.

    The examine command shows detailed game info about an
    object and optionally a specific attribute on it.
    If object is not specified, the current location is examined.

    Append a * before the search string to examine a player.

    """
    key = "@examine"
    locks = "cmd:pperm(examine) or pperm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"\s.*?|$"
