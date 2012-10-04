from ev import default_cmds

class CmdSysBoot(default_cmds.CmdBoot):
    """
    @boot

    Usage
      @boot[/switches] <player obj> [: reason]

    Switches:
      quiet - Silently boot without informing player
      port - boot by port number instead of name or dbref

    Boot a player object from the server. If a reason is
    supplied it will be echoed to the user unless /quiet is set.
    """

    key = "@boot"
    locks = "cmd:perm(boot) or perm(Wizards)"
    help_category = "Admin"

