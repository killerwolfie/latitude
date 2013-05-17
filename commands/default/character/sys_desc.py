from ev import default_cmds

class CmdSysDesc(default_cmds.CmdDesc):
    """
    @desc - describe an object or room

    Usage:
      @desc [<obj> =] >description>

    Setts the "desc" attribute on an
    object. If an object is not given,
    describe the current room.
    """
    key = "@desc"
    locks = "cmd:pperm(command_desc) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

