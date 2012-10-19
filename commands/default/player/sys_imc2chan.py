from ev import default_cmds

class CmdSysIMC2Chan(default_cmds.CmdIMC2Chan):
    """
    imc2chan - link an evennia channel to imc2

    Usage:
      @imc2chan[/switches] <evennia_channel> = <imc2_channel>

    Switches:
      /disconnect - this clear the imc2 connection to the channel.
      /remove     -                "
      /list       - show all imc2<->evennia mappings

    Example:
      @imc2chan myimcchan = ievennia

    Connect an existing evennia channel to a channel on an IMC2
    network. The network contact information is defined in settings and
    should already be accessed at this point. Use @imcchanlist to see
    available IMC channels.

    """

    key = "@imc2chan"
    locks = "cmd:serversetting(IMC2_ENABLED) and pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

