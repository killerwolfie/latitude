from ev import default_cmds, settings

class CmdSysAccess(default_cmds.MuxPlayerCommand):
    """
    access - show access groups

    Usage:
      @access

    This command shows you the permission hierarchy and
    which permission groups you are a member of.
    """
    key = "@access"
    locks = "cmd:all()"
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        self.msg('{wPermission Hierarchy{n (climbing): %s' % ', '.join(settings.PERMISSION_HIERARCHY))
        self.msg('{wYour access{n:')
        # Player
        if self.caller.is_superuser:
            pperms = "<Superuser>"
        else:
            pperms = ", ".join(self.caller.permissions)
        self.msg('  Player %s{n: %s' % (self.caller.return_styled_name(self.caller), pperms))
        # Character
        if not self.character:
            cperms = None
        elif self.character.is_superuser:
            cperms = "<Superuser>"
        else:
            cperms = ", ".join(self.character.permissions)
        if cperms:
            self.msg('  Character %s{n: %s' % (self.character.return_styled_name(self.caller), cperms))
