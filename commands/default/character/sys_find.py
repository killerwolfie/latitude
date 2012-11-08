from ev import default_cmds

class CmdSysFind(default_cmds.CmdFind):
    """
    find objects

    Usage:
      @find[/switches] <name or dbref or *player> [= dbrefmin[-dbrefmax]]

    Switches:
      room - only look for rooms (location=None)
      exit - only look for exits (destination!=None)
      char - only look for characters (BASE_CHARACTER_TYPECLASS)

    Searches the database for an object of a particular name or dbref.
    Use *playername to search for a player. The switches allows for
    limiting object matches to certain game entities. Dbrefmin and dbrefmax
    limits matches to within the given dbrefs, or above/below if only one is given.
    """

    key = "@find"
    aliases = "find, @search, search, @locate, locate"
    locks = "cmd:pperm(find) or pperm(Janitors)"
    help_category = "--- Coder/Sysadmin ---"

