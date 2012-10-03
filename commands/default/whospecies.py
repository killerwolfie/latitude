from ev import default_cmds
from ev import utils
import time

class CmdWhospecies(default_cmds.MuxCommand):
    """
    This sets up the basis for a Evennia's 'MUX-like' command
    style. The idea is that most other Mux-related commands should
    just inherit from this and don't have to implement parsing of
    their own unless they do something particularly advanced.

    A MUXCommand command understands the following possible syntax:

      name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

    The 'name[ with several words]' part is already dealt with by the
    cmdhandler at this point, and stored in self.cmdname. The rest is stored
    in self.args.

    The MuxCommand parser breaks self.args into its constituents and stores them in the
    following variables:
      self.switches = optional list of /switches (without the /)
      self.raw = This is the raw argument input, including switches
      self.args = This is re-defined to be everything *except* the switches
      self.lhs = Everything to the left of = (lhs:'left-hand side'). If
                 no = is found, this is identical to self.args.
      self.rhs: Everything to the right of = (rhs:'right-hand side').
                If no '=' is found, this is None.
      self.lhslist - self.lhs split into a list by comma
      self.rhslist - list of self.rhs split into a list by comma
      self.arglist = list of space-separated args (including '=' if it exists)

      All args and list members are stripped of excess whitespace around the
      strings, but case is preserved.
      """

    key = "whospecies"
    aliases = [ 'ws', 'whospe', 'whois' ]
    locks = "cmd:all()"
    help_category = "General"

    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.

    def func(self):
        characters = [ thing for thing in self.caller.location.contents if thing.player ]
        if "far" in self.switches:
            characters = [ thing for thing in self.caller.search(self.args, global_search=True, ignore_errors=True) if thing.player ]
        idle_threshhold = 180 # Three minutes minimum idle.

        num_asleep = 0
	num_awake = 0

        self.caller.msg("%cn%ccName                 Status  Gender    Species   %ch%cb[%ccws #help%cb for help]")
        self.caller.msg("%cn%ch%cw------------------------------------------------------------------------------")
        for character in characters:
            name = '%-20s' % character.key
	    name = name[:20]
	    if character.has_player:
	        name = '%cn%ch%cc' + name
	    else:
	        name = '%cn%cc' + name

            status = '%ch%cr?%cg?%cy?%cb?%cm?%cc?'
            if character.has_player:
                idle_time = time.time() - character.sessions[0].cmd_last_visible
                if idle_time < idle_threshhold:
                    status = '%ch%cgOK    '
                else:
                    status = '%ch%cwIdle  '
            else:
                status = '%cn%cgZzzz  '

            gender = character.db.desc_gender
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
        footer = "%%cn%%ch%%cw--%%cb[ %%cn%%cc%d%%ch%%cb players listed, comprising %%cn%%cc%d%%ch%%cb awake. ]%%cw-----------------------------------" % (num_awake + num_asleep, num_awake)
	footer = footer[:117]
        self.caller.msg(footer)

