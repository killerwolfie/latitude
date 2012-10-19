from src.server.sessionhandler import SESSIONS
from ev import default_cmds
from ev import utils
import time

class CmdSysWho(default_cmds.MuxCommand):
    """
    @who

      Display a table of basic information on other players.
    """

    key = "@who"
    locks = "cmd:all()"
    aliases = ['who', 'ws']
    help_category = "Information"

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

        self.caller.msg("%cn%ccName               Stamina   Gender    Species")
        self.caller.msg("%cn%ch%cw------------------------------------------------------------------------------")
	if not char_list:
	    self.caller.msg('%cn%crNo results')
        for character in char_list:
            name = '%-18s' % character.key
	    name = name[:18]
	    if character.has_player:
	        name = '%cn%ch%cc' + name
	    else:
	        name = '%cn%cc' + name

            status = '%cn%cw?%ch%cr?%cg?%cy?%cb?%cm?%cc?  '
            if character.has_player:
                idle_time = time.time() - character.sessions[0].cmd_last_visible
                if idle_time < idle_threshhold:
		    if character.db.stat_stamina != None and character.db.stat_stamina_max != None:
                        status = '%d/%d' % (character.db.stat_stamina, character.db.stat_stamina_max)
			status = '%-9s' % status
			fraction = float(character.db.stat_stamina) / float(character.db.stat_stamina_max)
			if fraction > 0.8:
			    status = '%ch%cg' + status
			elif fraction > 0.5:
			    status = '%cn%cg' + status
			elif fraction > 0.2:
			    status = '%ch%cy' + status
                        else:
			    status = '%cn%cr' + status
                else:
                    status = '%ch%cwIdle     '
            else:
                status = '%cn%cgZzzz     '

            gender = character.db.attr_gender
	    if gender:
                gender = '%-10s' % gender
	        gender = gender[:10]

	    if not gender:
	        gender = '%cn%cr-Unset-  '
            elif gender.lower().rstrip() in ['male', 'man', 'boy', 'dude', 'him']:
	        gender = '%cn%ch%cb' + gender
            elif gender.lower().rstrip() in ['female', 'woman', 'girl', 'chick', 'her']:
	        gender = '%cn%ch%cm' + gender
	    elif gender.lower().rstrip() in ['herm', 'hermy', 'both', 'shemale']:
	        gender = '%cn%ch%cg' + gender
	    else:
	        gender = '%cn%ch%cw' + gender

            species = character.db.desc_species
	    if species:
                species = '%-39s' % species
		species = species[:39]

	    if not species:
	        species = '%cn%cr-Unset-'
            else:
	        species = '%cn%ch%cw' + species

            self.caller.msg('%s %s %s %s' % (name, status, gender, species))

	    if character.has_player:
	        num_awake += 1
            else:
	        num_asleep += 1
        footer = "%%cn%%ch%%cw--%%cb[ %%cn%%cc%d%%ch%%cb players listed (%%cn%%cc%d%%ch%%cb awake) ]%%cw---------------------------------------------------------------------------------" % (num_awake + num_asleep, num_awake)
	footer = footer[:117]
        self.caller.msg(footer)

