from ev import default_cmds

class CmdSysEncoding(default_cmds.CmdEncoding):
    """
    encoding - set a custom text encoding

    Usage:
      @encoding/switches [<encoding>]

    Switches:
      clear - clear your custom encoding


    This sets the text encoding for communicating with Evennia. This is mostly an issue only if
    you want to use non-ASCII characters (i.e. letters/symbols not found in English). If you see
    that your characters look strange (or you get encoding errors), you should use this command
    to set the server encoding to be the same used in your client program.

    Common encodings are utf-8 (default), latin-1, ISO-8859-1 etc.

    If you don't submit an encoding, the current encoding will be displayed instead.
    """

    key = "@encoding"
    aliases = "@encode"
    locks = "cmd:all()"
    help_category = "General"
    arg_regex = r"(/\w+?(\s|$))|\s|$"
