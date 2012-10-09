from ev import default_cmds

class CmdSysServerLoad(default_cmds.CmdServerLoad):
    """
    server load and memory statistics

    Usage:
       @serverload

    This command shows server load statistics and dynamic memory
    usage.

    Some Important statistics in the table:

    {wServer load{n is an average of processor usage. It's usually
    between 0 (no usage) and 1 (100% usage), but may also be
    temporarily higher if your computer has multiple CPU cores.

    The {wResident/Virtual memory{n displays the total memory used by
    the server process.

    Evennia {wcaches{n all retrieved database entities when they are
    loaded by use of the idmapper functionality. This allows Evennia
    to maintain the same instances of an entity and allowing
    non-persistent storage schemes. The total amount of cached objects
    are displayed plus a breakdown of database object types. Finally,
    {wAttributes{n are cached on-demand for speed. The total amount of
    memory used for this type of cache is also displayed.

    """
    key = "@server"
    aliases = ["@serverload", "@serverprocess"]
    locks = "cmd:pperm(list) or pperm(Janitors)"
    help_category = "=== Admin ==="

