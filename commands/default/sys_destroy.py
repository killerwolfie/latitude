from ev import default_cmds

class CmdSysDestroy(default_cmds.CmdDestroy):
    """
    @destroy - remove objects from the game

    Usage:
       @destroy[/switches] [obj, obj2, obj3, [dbref-dbref], ...]

    switches:
       override - The @destroy command will usually avoid accidentally destroying
                  player objects. This switch overrides this safety.
    examples:
       @destroy house, roof, door, 44-78
       @destroy 5-10, flower, 45

    Destroys one or many objects. If dbrefs are used, a range to delete can be
    given, e.g. 4-10. Also the end points will be deleted.
    """

    key = "@destroy"
    aliases = ["@delete", "@del"]
    locks = "cmd:perm(destroy) or perm(Builders)"
    help_category = "Building"

