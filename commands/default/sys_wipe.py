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
    locks = "cmd:perm(wipe) or perm(Builders)"
    help_category = "Building"

