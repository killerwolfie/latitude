from ev import default_cmds

class CmdSysPerm(default_cmds.CmdPerm):
    """
    @perm - set permissions

    Usage:
      @perm[/switch] <object> [= <permission>[,<permission>,...]]
      @perm[/switch] *<player> [= <permission>[,<permission>,...]]

    Switches:
      del : delete the given permission from <object> or <player>.
      player : set permission on a player (same as adding * to name)

    This command sets/clears individual permission strings on an object
    or player. If no permission is given, list all permissions on <object>.
    """
    key = "@perm"
    aliases = "@setperm"
    locks = "cmd:pperm(command_@perm) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

    def func(self):
        "Implement function"

        caller = self.caller
        switches = self.switches
        lhs, rhs = self.lhs, self.rhs

        if not self.args:
            string = "Usage: @perm[/switch] object [ = permission, permission, ...]"
            caller.msg(string)
            return

        playermode = 'player' in self.switches or lhs.startswith('*')

        if playermode:
            obj = caller.search_player(lhs)
        else:
            obj =  caller.search(lhs, global_search=True)
        if not obj:
            return

        if not rhs:
            string = "Permissions on {w%s{n: " % obj.key
            if not obj.permissions:
                string += "<None>"
            else:
                string += ", ".join(obj.permissions)
                if hasattr(obj, 'player') and hasattr(obj.player, 'is_superuser') and obj.player.is_superuser:
                    string += "\n(... but this object is currently controlled by a SUPERUSER! "
                    string += "All access checks are passed automatically.)"
            caller.msg(string)
            return

        # we supplied an argument on the form obj = perm
        cstring = ""
        tstring = ""
        if 'del' in switches:
            # delete the given permission(s) from object.
            for perm in self.rhslist:
                try:
                    index = obj.permissions.index(perm)
                except ValueError:
                    cstring += "\nPermission '%s' was not defined on %s." % (perm, obj.name)
                    continue
                permissions = obj.permissions
                del permissions[index]
                obj.permissions = permissions
                cstring += "\nPermission '%s' was removed from %s." % (perm, obj.name)
                tstring += "\n%s revokes the permission '%s' from you." % (caller.name, perm)
        else:
            # add a new permission
            permissions = obj.permissions

            for perm in self.rhslist:

                # don't allow to set a permission higher in the hierarchy than the one the
                # caller has (to prevent self-escalation)
                if perm.lower() in PERMISSION_HIERARCHY and not obj.locks.check_lockstring(caller, "dummy:perm(%s)" % perm):
                    caller.msg("You cannot assign a permission higher than the one you have yourself.")
                    return

                if perm in permissions:
                    cstring += "\nPermission '%s' is already defined on %s." % (rhs, obj.name)
                else:
                    permissions.append(perm)
                    obj.permissions = permissions
                    cstring += "\nPermission '%s' given to %s." % (rhs, obj.name)
                    tstring += "\n%s gives you the permission '%s'." % (caller.name, rhs)
        caller.msg(cstring.strip())
        if tstring:
            obj.msg(tstring.strip())

