from ev import default_cmds

class CmdSysWipe(default_cmds.CmdWipe):
    """
    @wipe - clears attributes

    Usage:
      @wipe <object>[/attribute[/attribute...]]

    Example:
      @wipe box
      @wipe box/colour

    Wipes all of an object's attributes, or optionally only those
    matching the given attribute-wildcard search string.
    """
    key = "@wipe"
    locks = "cmd:perm(command_@wipe) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        """
        inp is the dict produced in ObjManipCommand.parse()
        """

        caller = self.caller

        if not self.args:
            caller.msg("Usage: @wipe <object>[/attribute/attribute...]")
            return

        # get the attributes set by our custom parser
        objname = self.lhs_objattr[0]['name']
        attrs = self.lhs_objattr[0]['attrs']

        obj = caller.search(objname)
        if not obj:
            return
        if not attrs:
            # wipe everything
            for attr in obj.get_all_attributes():
                attr.delete()
            string = "Wiped all attributes on %s." % obj.name
        else:
            for attrname in attrs:
                obj.attr(attrname, delete=True )
            string = "Wiped attributes %s on %s."
            string = string % (",".join(attrs), obj.name)
        caller.msg(string)

