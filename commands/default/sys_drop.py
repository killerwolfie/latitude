from ev import default_cmds

class CmdSysDrop(default_cmds.CmdDrop):
    """
    drop

    Usage:
      drop <obj>

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"

