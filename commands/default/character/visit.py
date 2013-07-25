from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import settings, search_object, create_script, utils
from game.gamesrc.latitude.utils.evennia_color import *
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

_AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))

class CmdVisit(LatitudeCommand):
    """
    visit - visit another area

    Usage:
      visit
      visit list
        List the areas in this region that you're eligable to visit.

      visit <area name>
        Visit the requested area.  Partial names will also work.
    """
    key = "visit"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        if not self.args or self.args.lower() == 'list':
            self.cmd_list()
            return
        else:
            self.cmd_visit()
            return

    def cmd_list(self):
        character = self.character
        region = character.get_region()
        visit_cost = region.db.region_visit_cost
        wander_cost = region.db.region_wander_cost
        areas_plain = []
        areas_reason = []
        # Header
        self.msg('-------------------------------------------------------------------------------')
        self.msg(evennia_color_center('{CRegion: {m%s   {CTravel Cost: %s%s   {CWander Cost: %s%s' % (
            region.key,
            self.satisfies_cost(visit_cost) and '{G' or '{R',
            visit_cost and conj_join([str(cost) + ' ' + attr for attr, cost in visit_cost.iteritems()], 'and') or '{GNone',
            self.satisfies_cost(wander_cost) and '{G' or '{R',
            wander_cost and conj_join([str(cost) + ' ' + attr for attr, cost in wander_cost.iteritems()], 'and') or '{GNone',
        ), 79))
        self.msg('  ---------------------------------------------------------------------------  ')
        # Get permissions (and returned reasons) for areas
        for area in region.contents:
            if not hasattr(area, 'can_visit'):
                continue
            reason = area.can_visit(character)
            if not reason:
                continue
            # Add this to the 'plain listing' section if applicable
            if 'Known' in reason or 'Landmark' in reason:
                areas_plain.append((area, reason))
            # Add this to the 'detailed reason listing' section if applicable
            reason_misc = reason
            if 'Known' in reason_misc:
                reason.remove('Known')
            if 'Landmark' in reason_misc:
                reason.remove('Landmark')
            if reason_misc:
                areas_reason.append((area, reason_misc))
        if not (areas_plain or areas_reason):
            self.msg('{R[There are no areas you can currently visit.]')
            return
        # Sort the list of areas
        areas_plain.sort(key=lambda area: (area[0].key, area[1]))
        areas_reason.sort(key=lambda area: (area[0].key, area[1]))
        # Display the list of areas
        for index in range(0, len(areas_plain), 3):
            self.msg('   '.join([evennia_color_left('{M' + area[0].key, 23) for area in areas_plain[index:index+3]]))
        if areas_plain and areas_reason:
            self.msg('  ---------------------------------------------------------------------------  ')
        for area, reason in areas_reason:
            self.msg('{M%s {C(%s{C)' % (area.key, '{C,'.join(reason)))
        # Footer
        self.msg('  ---------------------------------------------------------------------------  ')
        self.msg(evennia_color_center('{CUse visit <area name> to visit an area.', 79))
        self.msg('-------------------------------------------------------------------------------')

    def cmd_visit(self):
        character = self.character
        region = character.get_region()
        area = character.get_area()
        areas = [option for option in region.contents if hasattr(option, 'can_visit') and option.can_visit(character)]
        results = search_object(self.args, exact=False, candidates=areas)
        destination = _AT_SEARCH_RESULT(character, self.args, results, global_search=False, nofound_string="You can't find that area.", multimatch_string="More than one area matches '%s':" % (self.args))
        if not destination:
            return # The search result hook should have informed the user
        # Ensure the player has permission to leave this area
        if character.location:
            if not character.location.access(character, 'leave'):
                # The access check should display a message
                return
        # Ensure the user isn't trying to go where they already are
        if area == destination:
            self.msg("{Y[You're already in that area]")
            return
        # Ensure the user has enough points to travel
        visit_cost = region.db.region_visit_cost
        if not self.satisfies_cost(visit_cost):
            region.at_visit_insufficient(character)
            self.msg("You're too tired.")
            return
        # Move the character
        if character.get_room():
            prompt_script = create_script('game.gamesrc.latitude.scripts.prompt_leave.PromptLeave', obj=character, autostart=False)
            prompt_script.db.destination = destination
            prompt_script.db.cost = visit_cost
            prompt_script.db.followers = True
            prompt_script.db.yes_message = 'You head off in search of your destination.'
            prompt_script.db.no_message = 'You decide to stay where you are.'
            prompt_script.start()
        else:
            message = ['You head off in search of your destination.']
            if visit_cost:
                message = [character.game_attribute_offset(attr, -cost) for attr, cost in visit_cost.iteritems()]
            self.msg(' '.join(message))
            character.move_to(destination, redirectable=True, followers=False) # If you're in the region object, then you shouldn't have followers.  If you somehow do, then it's best you lose them now rather than drag them off.

    def satisfies_cost(self, attr_cost):
        character = self.character
        if attr_cost:
            for attr, cost in attr_cost.iteritems():
                if character.game_attribute_current(attr) < cost:
                    return False
        return True 
