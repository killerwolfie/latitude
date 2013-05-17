from ev import default_cmds

class CmdSysCreate(default_cmds.CmdCreate):
    """
    @create - create new objects

    Usage:
      @create[/drop] objname[;alias;alias...][:typeclass], objname...

    switch:
       drop - automatically drop the new object into your current location (this is not echoed)
              this also sets the new object's home to the current location rather than to you.

    Creates one or more new objects. If typeclass is given, the object
    is created as a child of this typeclass. The typeclass script is
    assumed to be located under game/gamesrc/types and any further
    directory structure is given in Python notation. So if you have a
    correct typeclass object defined in
    game/gamesrc/types/examples/red_button.py, you could create a new
    object of this type like this:

       @create button;red : examples.red_button.RedButton

    """

    key = "@create"
    locks = "cmd:perm(command_@create) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

