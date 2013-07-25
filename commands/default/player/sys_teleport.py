from ev import default_cmds

class CmdSysTeleport(default_cmds.CmdTeleport):
    """
    @tel - Change an object's location

    Usage:
      @tel[/switches] <location>
        Move yourself to a given location.

      @tel[/switches] <object>=<location>
        Move a given object to a given location.

    Switches:
      quiet
        Don't echo leave/arrive messages to the source/target locations for the
        move.

      intoexit
        If target is an exit, teleport INTO the exit object instead of to its
        destination
    """
    key = "@tel"
    aliases = "@teleport"
    locks = "cmd:perm(command_@teleport) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

