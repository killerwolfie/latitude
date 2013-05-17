from ev import default_cmds

class CmdSysDestroy(default_cmds.MuxCommand):
    """
    @destroy - remove objects from the game

    Usage:
       @destroy[/switches] [obj, obj2, obj3, [dbref-dbref], ...]

    switches:
       override - The @destroy command will usually avoid accidentally destroying
                  player objects. This switch overrides this safety.
    examples:
       @destroy house, roof, door, 44-78
       @destroy 5-10, flower, 45

    Destroys one or many objects. If dbrefs are used, a range to delete can be
    given, e.g. 4-10. Also the end points will be deleted.
    """

    key = "@destroy"
    locks = "cmd:pperm(command_@destroy) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

    def func(self):
        "Implements the command."

        caller = self.caller

        if not self.args or not self.lhslist:
            caller.msg("Usage: @destroy[/switches] [obj, obj2, obj3, [dbref-dbref],...]")
            return ""

        def delobj(objname, byref=False):
            # helper function for deleting a single object
            string = ""
            obj = caller.search(objname)
            if not obj:
                self.caller.msg(" (Objects to destroy must either be local or specified with a unique #dbref.)")
                return ""
            if not "override" in self.switches and obj.dbid == int(settings.CHARACTER_DEFAULT_HOME.lstrip("#")):
                return "\nYou are trying to delete CHARACTER_DEFAULT_HOME. If you want to do this, use the /override switch."
            objname = obj.name
            if obj.player and not 'override' in self.switches:
                return "\nObject %s is controlled by an active player. Use /override to delete anyway." % objname

            had_exits = hasattr(obj, "exits") and obj.exits
            had_objs = hasattr(obj, "contents") and any(obj for obj in obj.contents
                                                        if not (hasattr(obj, "exits") and obj not in obj.exits))
            # do the deletion
            okay = obj.delete()
            if not okay:
                string += "\nERROR: %s not deleted, probably because at_obj_delete() returned False." % objname
            else:
                string += "\n%s was destroyed." % objname
                if had_exits:
                    string += " Exits to and from %s were destroyed as well." % objname
                if had_objs:
                    string += " Objects inside %s were moved to their homes." % objname
            return string

        string = ""
        for objname in self.lhslist:
            if '-' in objname:
                # might be a range of dbrefs
                dmin, dmax = [utils.dbref(part, reqhash=False) for part in objname.split('-', 1)]
                if dmin and dmax:
                    for dbref in range(int(dmin),int(dmax+1)):
                        string += delobj("#" + str(dbref), True)
                else:
                    string += delobj(objname)
            else:
                string += delobj(objname, True)
        if string:
            caller.msg(string.strip())

