from src.server.sessionhandler import SESSIONS
from ev import utils
from game.gamesrc.latitude.utils.evennia_color import *
import string
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysWhereare(LatitudeCommand):
    """
    @whereare - View popular locations

    Usage:
      @whereare [<number>]
        Displays a list of the world's most popular locations, and any of your friends
        who may be there.  If a number is supplied, it shows locations with a minimum
        of that number of characters.
    """

    key = "@whereare"
    locks = "cmd:all()"
    aliases = ['wa']
    help_category = "Information"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        if self.args and self.args.isdigit():
            self.show_whereare(int(self.args))
        elif not self.args and not self.switches:
            # Default threshold is 5% of the server's population
            characters = 0
            for session in SESSIONS.get_sessions():
                if session.get_character():
                    characters += 1
            self.show_whereare(characters / 20)
        else:
            self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))

    def show_whereare(self, threshold):
        # Produce a list of locations
        locations = {}
        for session in SESSIONS.get_sessions():
            # Extract the location data
            character = session.get_character()
            if not character:
                continue
            character = character.typeclass
            location = character.location
            if not location or not hasattr(location, 'get_area'):
                continue
            area = location.get_area()
            if not area:
                continue
            region = area.get_region()
            if not region:
                continue
            # Add the location
            if not region in locations:
                locations[region] = {}
            if not area in locations[region]:
                locations[region][area] = {}
            if not location in locations[region][area]:
                locations[region][area][location] = set()
            locations[region][area][location].add(character)
        # Prune out locations that don't meet the threshold
        for region in locations.keys():
            for area in locations[region].keys():
                for location in locations[region][area].keys():
                    if len(locations[region][area][location]) < threshold:
                        del locations[region][area][location]
                if not locations[region][area]:
                    del locations[region][area]
            if not locations[region]:
                del locations[region]
        # Cache a list of friends
        my_friends = self.player.get_friend_characters(online_only=False)
        my_friends |= self.player.get_characters(online_only=False)
        # Output the results
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        if not locations:
            self.msg('  {RNo rooms with %d or more characters.' % (threshold))
        else:
            for region in locations:
                self.msg(' {C' + string.capwords(region.objsub('&0w')) + '{C:')
                for area in locations[region]:
                    self.msg('   {C' + string.capwords(area.objsub('&0w')) + '{C:')
                    for location in locations[region][area]:
                        # Display the location
                        self.msg(evennia_color_left('     {c' + location.key + '{n'  + ('.' * 79), 73, dots=True) + evennia_color_right('{g' + str(len(locations[region][area][location])), 4, dots=True))
                        # Generate character lists
                        characters_here = set(char for char in location.contents if utils.inherits_from(char, "src.objects.objects.Character"))
                        friends_here = characters_here & my_friends
                        strangers_here = characters_here - friends_here
                        # Display character lists
                        charline = '       {x: Characters :{n '
                        if friends_here:
                            charline += '{n, '.join([friend.get_desc_styled_name(self.player) for friend in friends_here])
                            if strangers_here:
                                charline += '{n, plus '
                            else:
                                charline += '{n.'
                        if strangers_here:
                            charline += '{n%d awake and %d asleep.' % (len([stranger for stranger in strangers_here if stranger.sessid]), len([stranger for stranger in strangers_here if not stranger.sessid]))
                        self.msg(charline)
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
