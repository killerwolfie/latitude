from ev import default_cmds

class CmdSysIC(default_cmds.CmdIC):
    """
    Switch control to an object

    Usage:
      @ic <character>

    Go in-character (IC) as a given Character.

    This will attempt to "become" a different object assuming you have
    the right to do so.  You cannot become an object that is already
    controlled by another player. In principle <character> can be
    any in-game object as long as you have access right to puppet it.
    """

    key = "@ic"
    locks = "cmd:all()" # must be all() or different puppeted objects won't be able to access it.
    aliases = "@puppet"
    help_category = "General"

