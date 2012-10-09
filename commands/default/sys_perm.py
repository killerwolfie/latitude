from ev import default_cmds

class CmdSysPerm(default_cmds.CmdPerm):
    """
    @perm - set permissions

    Usage:
      @perm[/switch] <object> [= <permission>[,<permission>,...]]
      @perm[/switch] *<player> [= <permission>[,<permission>,...]]

    Switches:
      del : delete the given permission from <object> or <player>.
      player : set permission on a player (same as adding * to name)

    This command sets/clears individual permission strings on an object
    or player. If no permission is given, list all permissions on <object>.
    """
    key = "@perm"
    aliases = "@setperm"
    locks = "cmd:pperm(perm) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

