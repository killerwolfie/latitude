from src.server.sessionhandler import SESSIONS
from ev import default_cmds
from ev import utils
from game.gamesrc.latitude.utils.evennia_color import *
from game.gamesrc.latitude.utils.search import match, match_character

class CmdSysWho(default_cmds.MuxCommand):
    """
    @who - Display a table of basic information on other characters

    Usage:
      @who
      @who/characters
          List all connected characters
      @who/players
          List all connected players
      @who/room
      ws
          Lists everyone in your current room
      @who/far <character/player>
          Shows information on a specific character/player
    """

    key = "@who"
    locks = "cmd:all()"
    aliases = ['who', 'ws']
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        switches = [switch.lower() for switch in self.switches]
        caller = self.caller
        if self.cmdstring.lower() == 'ws':
            if not switches and not self.args:
                self.display_users([ con for con in self.caller.location.contents if utils.inherits_from(con, "src.objects.objects.Character") ])
                return
        else:
            if (not switches or switches == ['characters']) and not self.args:
                characters = set()
                for session in SESSIONS.get_sessions():
                    character = session.get_character()
                    if character:
                        character = character.typeclass
                        characters.add(character)
                self.display_users(characters)
                return
            if switches == ['players'] and not self.args:
                players = set()
                for session in SESSIONS.get_sessions():
                    player = session.get_player()
                    if player:
                        player = player.typeclass
                        players.add(player)
                self.display_users(players)
                return
            if switches == ['far'] and self.args:
                target = match(self.args)
                if not target:
                    self.caller.msg('%cnNo match found for "' + self.args + "'")
                    return
                self.display_users([target])
                return
            if switches == ['room'] and not self.args:
                self.display_users([ con for con in self.caller.location.contents if utils.inherits_from(con, "src.objects.objects.Character") ])
                return
        self.msg("Invalid '%s' command.  See 'help %s' for usage" % (self.cmdstring, self.key))

    def display_users(self, users):
        """
        Displays a listing of characters, players, or some combination thereof.

        Characters will also show game related status information, and players will not.
        As a result, if the users are nothing but players, a different header will display.
        """
        idle_threshhold = 180 # Three minutes minimum idle.
        num_asleep = 0
	num_awake = 0
        # Sort the list
        users = sorted(users, key=lambda user: (utils.inherits_from(user, "src.objects.objects.Character"), user.status_idle()))
        # Output the header
        has_characters = False
        for user in users:
            if utils.inherits_from(user, "src.objects.objects.Character"):
                has_characters = True
                break
        if has_characters:
            self.caller.msg("{CName                Stamina  Gender    Species           {b[{chelp @who{b for help]")
            self.caller.msg("{w------------------------------------------------------------------------------")
        else:
            self.caller.msg("{CName     {b[{chelp @who{b for help]")
            self.caller.msg("{w-----------------------------")
        # Output the body
	if not users:
	    self.caller.msg('{RNo results')
        for user in users:
            if not utils.inherits_from(user, "src.objects.objects.Character"):
                num_awake += 1
                # Player name
                name = user.return_title(self.caller)
                # Status
                status = '%cn%cw?%ch%cr?%cg?%cy?%cb?%cm?%cc?'
                if user.status_online():
                    idle_time = int(user.status_idle())
                    if idle_time < idle_threshhold:
                        status = '{gOnline'
                    else:
                        status = self.idle_string(idle_time)
                else:
                    status = '{GOffline'
                self.caller.msg('%s %s' % (evennia_color_left(name, 19, dots=True), evennia_color_left(status, 8)))
            else:
                # Character Name
                name = user.return_title(self.caller)
                # Stamina / Status readout
                stamina = '%cn%cw?%ch%cr?%cg?%cy?%cb?%cm?%cc?'
                if user.status_online():
                    idle_time = int(user.status_idle())
                    if idle_time < idle_threshhold:
                        if user.db.stat_stamina != None and user.db.stat_stamina_max != None:
                            stamina = '%d/%d' % (user.db.stat_stamina, user.db.stat_stamina_max)
                            fraction = float(user.db.stat_stamina) / float(user.db.stat_stamina_max)
                            if fraction > 0.8:
                                sstamina = '%ch%cg' + stamina
                            elif fraction > 0.5:
                                stamina = '%cn%cg' + stamina
                            elif fraction > 0.2:
                                stamina = '%ch%cy' + stamina
                            else:
                                stamina = '%cn%cr' + stamina
                    else:
                        stamina = self.idle_string(idle_time)
                else:
                    stamina = '%cn%cgZzzz'
                # Gender
                gender = user.db.attr_gender
                if not gender:
                    gender = '%cn%cr-Unset-'
                elif user.is_male():
                    gender = '%cn%ch%cb' + gender
                elif user.is_female():
                    gender = '%cn%ch%cm' + gender
                elif user.is_herm():
                    gender = '%cn%ch%cg' + gender
                else:
                    gender = '%cn%ch%cw' + gender
                # Species
                species = user.db.desc_species
                if not species:
                    species = '%cn%cr-Unset-'
                else:
                    species = '%cn%ch%cw' + species

                self.caller.msg('%s %s %s %s' % (evennia_color_left(name, 19, dots=True), evennia_color_left(stamina, 8), evennia_color_left(gender, 9, dots=True), evennia_color_left(species, 39, dots=True)))

                if user.has_player:
                    num_awake += 1
                else:
                    num_asleep += 1
        footer = EvenniaColorCanvas()
        if has_characters:
            footer.evennia_import('{w------------------------------------------------------------------------------')
            footer.draw_string(3, 0, '{b[ {C%s{b players listed ({C%d{b awake) ]' % (num_awake + num_asleep, num_awake))
        else:
            footer.evennia_import("{w-----------------------------")
            footer.draw_string(3, 0, '{b[ {C%s{b players ]' % (num_awake))
        self.caller.msg(footer.evennia_export())

    def idle_string(self, seconds):
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
        return '{wi{y%s{R%c' % (str(seconds), unit)
