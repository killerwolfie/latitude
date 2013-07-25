from ev import default_cmds

class CmdSysObjects(default_cmds.CmdObjects):
    """
    Give a summary of object types in database

    Usage:
      @objects [<nr>]
        Gives statictics on objects in database as well as a list of <nr> latest
        objects in database. If not given, <nr> defaults to 10.
    """
    key = "@objects"
    aliases = []
    locks = "cmd:perm(command_@objects) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

