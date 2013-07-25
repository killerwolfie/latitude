from ev import default_cmds

class CmdSysFind(default_cmds.CmdFind):
    """
    find objects - Search for an object by name or dbref

    Usage:
      @find <name or dbref> [= dbrefmin[-dbrefmax]]
        Search for an Object

      @find/room <*player> [= dbrefmin[-dbrefmax]]
        Search for a Player

      @find/room <name or dbref> [= dbrefmin[-dbrefmax]]
        Search for a room Object

      @find/exit <name or dbref> [= dbrefmin[-dbrefmax]]
        Search for an exit Object

      @find/char <name or dbref> [= dbrefmin[-dbrefmax]]
        Search for a character Object
    """

    key = "@find"
    aliases = "find, @search, search, @locate, locate"
    locks = "cmd:perm(command_@find) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

