from src.server.sessionhandler import SESSIONS
from ev import utils
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSys3Who(LatitudeCommand):
    """
    @3who - Display a list of online characters

    Usage:
      @3who
        Displays a list of players, with idle time and online time, in three
        columns.
    """
    key = "@3who"
    locks = "cmd:all()"
    aliases = ['3w', '3who']
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        char_num = 0
        output = "{x________________{W_______________{w_______________{W_______________{x_________________\n"
        output += '%cnName         OnTime Idle  Name         OnTime Idle  Name         Ontime Idle\n'
        output += '\n'
        for session in SESSIONS.get_sessions():
            character = session.get_character()
            if not character:
                continue
            char_num += 1
            name = character.key
            onseconds = int(character.status_online())
            onminutes = onseconds / 60
            ontime = '%02d:%02d' % (onminutes / 60, onminutes % 60)
            idletime = self.tdelta_string(int(character.status_idle()))
            output += '%-12s %6s %-5s ' % (name[:12], ontime[:6], idletime[:5])
            if char_num and char_num % 3 == 0:
                output += '\n'
        if not output.endswith('\n'):
            output += '\n'
        output += "{x________________{W_______________{w_______________{W_______________{x_________________\n"
        self.msg(output.rstrip('\n'))

    def tdelta_string(self, seconds):
        unit_table = [
            (60, 'm'),
            (60, 'h'),
            (24, 'd'),
            (365, 'y'),
        ]

        unit = 's'
        for entry in unit_table:
            if seconds / entry[0] == 0:
                break
            unit = entry[1]
            seconds = seconds / entry[0]
        return '%2s%c' % (str(seconds), unit)
