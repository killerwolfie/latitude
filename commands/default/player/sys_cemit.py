from ev import default_cmds

class CmdSysCemit(default_cmds.CmdCemit):
    """
    @cemit - send a message to channel

    Usage:
      @cemit[/switches] <channel> = <message>

    Switches:
      noheader - don't show the [channel] header before the message
      sendername - attach the sender's name before the message
      quiet - don't echo the message back to sender

    Allows the user to broadcast a message over a channel as long as
    they control it. It does not show the user's name unless they
    provide the /sendername switch.

    """

    key = "@cemit"
    aliases = []
    locks = "cmd:pperm(command_sys_cemit) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

