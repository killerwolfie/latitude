from ev import default_cmds

class CmdSysMvAttr(default_cmds.CmdMvAttr):
    """
    @mvattr - move attributes

    Usage:
      @mvattr[/switch] <obj>/<attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
      @mvattr[/switch] <obj>/<attr> = <obj1> [,<obj2>,<obj3>,...]
      @mvattr[/switch] <attr> = <obj1>/<attr1> [,<obj2>/<attr2>,<obj3>/<attr3>,...]
      @mvattr[/switch] <attr> = <obj1>[,<obj2>,<obj3>,...]

    Switches:
      copy - Don't delete the original after moving.

    Move an attribute from one object to one or more attributes on another object. If
    you don't supply a source object, yourself is used.
    """
    key = "@mvattr"
    locks = "cmd:pperm(command_@mvattr) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

