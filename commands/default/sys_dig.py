from ev import default_cmds

class CmdSysDig(default_cmds.CmdDig):
    """
    @dig - build and connect new rooms to the current one

    Usage:
      @dig[/switches] roomname[;alias;alias...][:typeclass]
            [= exit_to_there[;alias][:typeclass]]
               [, exit_to_here[;alias][:typeclass]]

    Switches:
       tel or teleport - move yourself to the new room

    Examples:
       @dig kitchen = north;n, south;s
       @dig house:myrooms.MyHouseTypeclass
       @dig sheer cliff;cliff;sheer = climb up, climb down

    This command is a convenient way to build rooms quickly; it creates the new room and you can optionally
    set up exits back and forth between your current room and the new one. You can add as many aliases as you
    like to the name of the room and the exits in question; an example would be 'north;no;n'.
    """
    key = "@dig"
    locks = "cmd:perm(dig) or perm(Builders)"
    help_category = "Building"

