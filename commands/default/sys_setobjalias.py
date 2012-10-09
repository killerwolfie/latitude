from ev import default_cmds

class CmdSysSetObjAlias(default_cmds.CmdSetObjAlias):
    """
    Adding permanent aliases

    Usage:
      @alias <obj> [= [alias[,alias,alias,...]]]

    Assigns aliases to an object so it can be referenced by more
    than one name. Assign empty to remove all aliases from object.
    Observe that this is not the same thing as aliases
    created with the 'alias' command! Aliases set with @alias are
    changing the object in question, making those aliases usable
    by everyone.
    """

    key  = "@alias"
    aliases = "@setobjalias"
    locks = "cmd:perm(setobjalias) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

