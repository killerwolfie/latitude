from ev import default_cmds

class CmdSysTunnel(default_cmds.CmdTunnel):
    """
    dig in often-used directions

    Usage:
      @tunnel[/switch] <direction> [= roomname[;alias;alias;...][:typeclass]]

    Switches:
      oneway - do not create an exit back to the current location
      tel - teleport to the newly created room

    Example:
      @tunnel n
      @tunnel n = house;mike's place;green building

    This is a simple way to build using pre-defined directions:
     {wn,ne,e,se,s,sw,w,nw{n (north, northeast etc)
     {wu,d{n (up and down)
     {wi,o{n (in and out)
    The full names (north, in, southwest, etc) will always be put as
    main name for the exit, using the abbreviation as an alias (so an
    exit will always be able to be used with both "north" as well as
    "n" for example). Opposite directions will automatically be
    created back from the new room unless the /oneway switch is given.
    For more flexibility and power in creating rooms, use @dig.
    """

    key = "@tunnel"
    aliases = ["@tun"]
    locks = "cmd: perm(tunnel) or perm(Builders)"
    help_category = "Building"

    # store the direction, full name and its opposite
    directions = {"n" : ("north", "s"),
                  "ne": ("northeast", "sw"),
                  "e" : ("east", "w"),
                  "se": ("southeast", "nw"),
                  "s" : ("south", "n"),
                  "sw": ("southwest", "ne"),
                  "w" : ("west", "e"),
                  "nw": ("northwest", "se"),
                  "u" : ("up", "d"),
                  "d" : ("down", "u"),
                  "i" : ("in", "o"),
                  "o" : ("out", "i")}

