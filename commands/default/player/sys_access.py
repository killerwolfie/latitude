from ev import settings
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysAccess(LatitudeCommand):
    """
    access - Show access groups

    Usage:
      @access
        This command shows you the permission hierarchy and which permission
        groups you are a member of.
    """
    key = "@access"
    locks = "cmd:all()"
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        self.msg('{CPermission Hierarchy (climbing): {n%s' % ', '.join(settings.PERMISSION_HIERARCHY))
        self.msg('{CYour access:')
        # Player
        if self.player.is_superuser:
            pperms = "<Superuser>"
        else:
            pperms = ", ".join(self.player.permissions)
        self.msg('  Player %s{n: %s' % (self.player.get_desc_styled_name(self.player), pperms))
        # Character
        if not self.character:
            cperms = None
        elif self.character.is_superuser:
            cperms = "<Superuser>"
        else:
            cperms = ", ".join(self.character.permissions)
        if cperms:
            self.msg('  Character %s{n: %s' % (self.character.get_desc_styled_name(self.player), cperms))
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
