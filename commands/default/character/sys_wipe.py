from ev import default_cmds

class CmdSysWipe(default_cmds.CmdWipe):
    """
    @wipe - clears attributes

    Usage:
      @wipe <object>[/attribute[/attribute...]]

    Example:
      @wipe box
      @wipe box/colour

    Wipes all of an object's attributes, or optionally only those
    matching the given attribute-wildcard search string.
    """
    key = "@wipe"
    locks = "cmd:pperm(wipe) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

