from ev import default_cmds

class CmdSysCopy(default_cmds.CmdCopy):
    """
    @copy - copy objects

    Usage:
      @copy[/reset] <original obj> [= new_name][;alias;alias..][:new_location] [,new_name2 ...]

    switch:
      reset - make a 'clean' copy off the object, thus
              removing any changes that might have been made to the original
              since it was first created.

    Create one or more copies of an object. If you don't supply any targets, one exact copy
    of the original object will be created with the name *_copy.
    """

    key = "@copy"
    locks = "cmd:perm(command_@copy) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

