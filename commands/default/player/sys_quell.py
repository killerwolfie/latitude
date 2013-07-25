from ev import default_cmds

class CmdSysQuell(default_cmds.CmdQuell):
    """
    @quell - Quell permissions

    Usage:
      @quell
        Normally the permission level of the Player is used when puppeting a
        Character/Object to determine access. This command will switch the lock
        system to make use of the puppeted Object's permissions instead. This is
        useful mainly for testing.
        Hierarchical permission quelling only work downwards, thus a Player cannot
        use a higher-permission Character to escalate their permission level.

      @unquell
        Use the @unquell command to revert back to normal operation.

    Note:
      The superuser character cannot be quelled. Use a separate admin account for
      testing.
    """

    key = "@quell"
    aliases =["@unquell"]
    locks = "cmd:pperm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"
