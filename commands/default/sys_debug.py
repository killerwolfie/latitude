from ev import default_cmds

class CmdSysDebug(default_cmds.CmdDebug):
    """
    Debug game entities

    Usage:
      @debug[/switch] <path to code>

    Switches:
      obj - debug an object
      script - debug a script

    Examples:
      @debug/script game.gamesrc.scripts.myscript.MyScript
      @debug/script myscript.MyScript
      @debug/obj examples.red_button.RedButton

    This command helps when debugging the codes of objects and scripts.
    It creates the given object and runs tests on its hooks.
    """

    key = "@debug"
    locks = "cmd:perm(debug) or perm(Builders)"
    help_category = "Building"

