from src.commands.default import building

class CmdSysHome(building.CmdHome):
    """
    @home - control an object's home location

    Usage:
      @home <obj> [= home_location]

    The "home" location is a "safety" location for objects; they
    will be moved there if their current location ceases to exist. All
    objects should always have a home location for this reason.
    It is also a convenient target of the "home" command.

    If no location is given, just view the object's home location.
    """

    key = "@home"
    locks = "cmd:perm(@home) or perm(Builders)"
    help_category = "Building"
