from ev import default_cmds

class CmdSysSay(default_cmds.CmdSay):
    """
    say

    Usage:
      say <message>

    Talk to those in your current location.
    """

    key = "say"
    aliases = ['"', "'"]
    locks = "cmd:all()"

