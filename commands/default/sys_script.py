from ev import default_cmds

class CmdSysScript(default_cmds.CmdScript):
    """
    attach scripts

    Usage:
      @script[/switch] <obj> [= <script.path or scriptkey>]

    Switches:
      start - start all non-running scripts on object, or a given script only
      stop - stop all scripts on objects, or a given script only

    If no script path/key is given, lists all scripts active on the given
    object.
    Script path can be given from the base location for scripts as given in
    settings. If adding a new script, it will be started automatically (no /start
    switch is needed). Using the /start or /stop switches on an object without
    specifying a script key/path will start/stop ALL scripts on the object.
    """

    key = "@script"
    aliases = "@addscript"
    locks = "cmd:pperm(script) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

