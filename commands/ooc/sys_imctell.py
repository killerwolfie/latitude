from ev import default_cmds

class CmdSysIMCTell(default_cmds.CmdIMCTell):
    """
    imctell - send a page to a remote IMC player

    Usage:
      imctell User@MUD = <msg>
      imcpage      "

    Sends a page to a user on a remote MUD, connected
    over IMC2.
    """

    key = "imctell"
    aliases = ["imcpage", "imc2tell", "imc2page"]
    locks = "cmd: serversetting(IMC2_ENABLED)"
    help_category = "Comms"

