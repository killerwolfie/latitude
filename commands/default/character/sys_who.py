from src.server.sessionhandler import SESSIONS
from ev import default_cmds
from ev import utils
import time
from game.gamesrc.latitude.utils import evennia_color

class CmdSysWho(default_cmds.MuxCommand):
    """
    @who - Display a table of basic information on other characters

    Usage:
      @who - Lists everyone on the server who's connected
      @who/room - Lists everyone in your current room (The default if you use the 'ws' command.)
      @who/far <character> - Shows information on a specific character
    """

    key = "@who"
    locks = "cmd:all()"
    aliases = ['who', 'ws']
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.

    def func(self):
        if 'far' in self.switches:
	    search_results = self.caller.search(self.args, global_search=True, ignore_errors=True)
            if search_results:
	        search_results = [thing for thing in search_results if thing.player]
	    else:
	        self.caller.msg('%cnNo results found for "' + self.args + "'")
	        search_results = []
	    self.display_users(search_results)
	elif 'room' in self.switches or self.cmdstring == 'ws':
            self.display_users([ thing for thing in self.caller.location.contents if thing.player ])
	else:
	    char_list = []
	    for session in SESSIONS.get_sessions():
	        character = session.get_character()
		if character:
		    char_list.append(character)
            self.display_users(set(char_list))
	    

    def display_users(self, char_list):
        if not char_list:
	    # There should never be a situation where you list a room or the whole server and get nobody.
	    # Otherwise, if you get to this point, there should have already been some error output.
	    return()
        idle_threshhold = 180 # Three minutes minimum idle.
        num_asleep = 0
	num_awake = 0
        self.caller.msg("{CName                Stamina  Gender    Species   {b[{chelp @who{b for help]")
        self.caller.msg("{w------------------------------------------------------------------------------")
	if not char_list:
	    self.caller.msg('{RNo results')
        for character in char_list:
            # Character Name
            name = character.key
            if character.has_player:
                name = '%cn%ch%cc' + name
            else:
                name = '%cn%cc' + name
            # Stamina / Status readout
            stamina = '%cn%cw?%ch%cr?%cg?%cy?%cb?%cm?%cc?'
            if character.has_player:
                idle_time = int(time.time() - character.sessions[0].cmd_last_visible)
                if idle_time < idle_threshhold:
		    if character.db.stat_stamina != None and character.db.stat_stamina_max != None:
                        stamina = '%d/%d' % (character.db.stat_stamina, character.db.stat_stamina_max)
			fraction = float(character.db.stat_stamina) / float(character.db.stat_stamina_max)
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
            gender = character.db.attr_gender
	    if not gender:
	        gender = '%cn%cr-Unset-'
            elif character.is_male():
	        gender = '%cn%ch%cb' + gender
            elif character.is_female():
	        gender = '%cn%ch%cm' + gender
	    elif character.is_herm():
	        gender = '%cn%ch%cg' + gender
	    else:
	        gender = '%cn%ch%cw' + gender
            # Species
            species = character.db.desc_species
	    if not species:
	        species = '%cn%cr-Unset-'
            else:
	        species = '%cn%ch%cw' + species

            self.caller.msg('%s %s %s %s' % (evennia_color.evennia_color_left(name, 19, dots=True), evennia_color.evennia_color_left(stamina, 8), evennia_color.evennia_color_left(gender, 9, dots=True), evennia_color.evennia_color_left(species, 39, dots=True)))

	    if character.has_player:
	        num_awake += 1
            else:
	        num_asleep += 1
        footer = evennia_color.EvenniaColorCanvas()
        footer.evennia_import('{w------------------------------------------------------------------------------')
        footer.draw_string(3, 0, '{b[ {C%s{b players listed ({C%d{b awake) ]' % (num_awake + num_asleep, num_awake))
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
