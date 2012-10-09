from ev import default_cmds

class CmdSysIMCPage(default_cmds.CmdIMCTell):
    """
    @imcpage - send a page to a remote IMC player

    Usage:
      @imcpage User@MUD = <msg>

    Sends a page to a user on a remote MUD, connected
    over IMC2.
    """

    key = "@imcpage"
    aliases = ["@imcpage"]
    locks = "cmd: serversetting(IMC2_ENABLED)"
    help_category = "Communication"

