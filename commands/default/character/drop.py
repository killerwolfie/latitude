from ev import default_cmds

class CmdDrop(default_cmds.CmdDrop):
    """
    drop

    Usage:
      drop <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    arg_regex = r"\s.*?|$"
    locks = "cmd:all()"
    help_category = "Actions"
