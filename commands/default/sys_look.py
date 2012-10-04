from ev import default_cmds

class CmdSysLook(default_cmds.CmdLook):
    """
    look

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"

