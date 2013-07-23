from ev import default_cmds, utils
from game.gamesrc.latitude.utils.search import match, match_character
import time

class CmdSysLast(default_cmds.MuxPlayerCommand):
    """
    @last

    Show a player's last login time, or the time a character was last used.

    Usage:
      @last <player/character>
    """

    key = "@last"
    locks = "cmd:all()"
    aliases = ['last', 'laston']
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        if not self.switches and self.args:
            target = match(self.args)
            if not target:
                self.msg('{R[Could not find "%s"]' % self.args)
                return
            if utils.inherits_from(target, "src.objects.objects.Character"):
                if target.sessid:
                    self.msg('{Y[%s is online right now]' % (target.key))
                elif not target.has_attribute('stats_last_unpuppet_time'):
                    self.msg('{R[The time %s last left the game is unknown]' % (target.key))
                elif target.db.stats_last_unpuppet_time == None:
                    self.msg('{Y[%s has never entered the game]' % (target.key))
                else:
                    self.msg('{Y[%s last left the game at %s]' % (target.key, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(target.db.stats_last_unpuppet_time))))
            else:
                if target.sessions:
                    self.msg('{Y[%s is online right now]' % (target.key))
                elif not target.has_attribute('stats_last_logout_time'):
                    self.msg('{R[The time %s last left the game is unknown]' % (target.key))
                elif target.db.stats_last_logout_time == None:
                    self.msg('{Y[%s has never entered the game]' % (target.key))
                else:
                    self.msg('{Y[%s last left the game at %s]' % (target.key, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(target.db.stats_last_logout_time))))
        else:
            # Unrecognized command
            self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))
