from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand
from ev import managers

class CmdSysIssues(LatitudeCommand):
    """
    @issues - List known problem

    Usage:
      @issues
        Display all known problems uncovered by background audit processes
    """
    key = "@issues"
    locks = "cmd:perm(command_@issues) or perm(Janitors)"
    aliases = []
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        issues = []
        # Grab the audit script
        audit_script = managers.scripts.typeclass_search('game.gamesrc.latitude.scripts.audit.Audit')
        if not audit_script:
            self.msg('{R[No audit script found]')
        elif len(audit_script) > 1:
            self.msg('{R[Multiple audit scripts found]')
        audit_script = audit_script[0]
        # Check bad objects
        known_bad = audit_script.db.audit_known_bad
        if known_bad:
            for obj in known_bad:
                if not obj:
                    continue
                reason = obj.bad()
                if not reason:
                    continue
                issues.append('"%s" %s(%s) %r' % (reason, obj.key, obj.dbref, obj))
        # Dispaly issues
        if not issues:
            self.msg('{G[There are currently no known issues]')
        else:
            self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
            self.msg('\n'.join(issues))
            self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
