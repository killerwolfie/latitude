from ev import default_cmds

class CmdSysAlias(default_cmds.CmdSetObjAlias):
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
    aliases = []
    locks = "cmd:perm(command_@alias) or perm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        "Set the aliases."

        caller = self.caller

        if not self.lhs:
            string = "Usage: @alias <obj> [= [alias[,alias ...]]]"
            self.caller.msg(string)
            return
        objname = self.lhs

        # Find the object to receive aliases
        obj = caller.search(objname)
        if not obj:
            return
        if self.rhs == None:
            # no =, so we just list aliases on object.
            aliases = obj.aliases
            if aliases:
                caller.msg("Aliases for '%s': %s" % (obj.key, ", ".join(aliases)))
            else:
                caller.msg("No aliases exist for '%s'." % obj.key)
            return

        if not self.rhs:
            # we have given an empty =, so delete aliases
            old_aliases = obj.aliases
            if old_aliases:
                caller.msg("Cleared aliases from %s: %s" % (obj.key, ", ".join(old_aliases)))
                del obj.dbobj.aliases
            else:
                caller.msg("No aliases to clear.")
            return

        # merge the old and new aliases (if any)
        old_aliases = obj.aliases
        new_aliases = [alias.strip().lower() for alias in self.rhs.split(',') if alias.strip()]
        # make the aliases only appear once
        old_aliases.extend(new_aliases)
        aliases = list(set(old_aliases))
        # save back to object.
        obj.aliases = aliases
        # we treat this as a re-caching (relevant for exits to re-build their exit commands with the correct aliases)
        caller.msg("Aliases for '%s' are now set to %s." % (obj.key, ", ".join(obj.aliases)))

