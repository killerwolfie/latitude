from ev import default_cmds

class CmdSysTypeclass(default_cmds.CmdTypeclass):
    """
    @typeclass - set object typeclass

    Usage:
      @typclass[/switch] <object> [= <typeclass.path>]
      @type                     ''
      @parent                   ''

    Switch:
      reset - clean out *all* the attributes on the object -
              basically making this a new clean object.
      force - change to the typeclass also if the object
              already has a typeclass of the same name.
    Example:
      @type button = examples.red_button.RedButton

    View or set an object's typeclass. If setting, the creation hooks
    of the new typeclass will be run on the object. If you have
    clashing properties on the old class, use /reset. By default you
    are protected from changing to a typeclass of the same name as the
    one you already have, use /force to override this protection.

    The given typeclass must be identified by its location using
    python dot-notation pointing to the correct module and class. If
    no typeclass is given (or a wrong typeclass is given). Errors in
    the path or new typeclass will lead to the old typeclass being
    kept. The location of the typeclass module is searched from the
    default typeclass directory, as defined in the server settings.

    """

    key = "@typeclass"
    locks = "cmd:perm(command_@typeclass) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        "Implements command"

        caller = self.caller

        if not self.args:
            caller.msg("Usage: @type <object> [=<typeclass]")
            return

        # get object to swap on
        obj = caller.search(self.lhs)
        if not obj:
            return

        if not self.rhs:
            # we did not supply a new typeclass, view the
            # current one instead.
            if hasattr(obj, "typeclass"):
                string = "%s's current typeclass is '%s' (%s)." % (obj.name, obj.typeclass.typename, obj.typeclass.path)
            else:
                string = "%s is not a typed object." % obj.name
            caller.msg(string)
            return

        # we have an =, a typeclass was supplied.
        typeclass = self.rhs

        if not hasattr(obj, 'swap_typeclass') or not hasattr(obj, 'typeclass'):
            caller.msg("This object cannot have a type at all!")
            return

        is_same = obj.is_typeclass(typeclass)
        if is_same and not 'force' in self.switches:
            string = "%s already has the typeclass '%s'. Use /force to override." % (obj.name, typeclass)
        else:
            reset = "reset" in self.switches
            old_typeclass_path = obj.typeclass.path
            ok = obj.swap_typeclass(typeclass, clean_attributes=reset)
            if ok:
                if is_same:
                    string = "%s updated its existing typeclass (%s).\n" % (obj.name, obj.typeclass.path)
                else:
                    string = "%s's changed typeclass from %s to %s.\n" % (obj.name,
                                                                         old_typeclass_path,
                                                                         obj.typeclass.path)
                string += "Creation hooks were run."
                if reset:
                    string += " All old attributes where deleted before the swap."
                else:
                    string += " Note that the typeclassed object could have ended up with a mixture of old"
                    string += "\nand new attributes. Use /reset to remove old attributes if you don't want this."
            else:
                string = obj.typeclass_last_errmsg
                string += "\nCould not swap '%s' (%s) to typeclass '%s'." % (obj.name,
                                                                          old_typeclass_path,
                                                                          typeclass)

        caller.msg(string)

