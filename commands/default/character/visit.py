from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import default_cmds, settings, search_object, create_script, utils

_AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))

class CmdVisit(default_cmds.MuxPlayerCommand):
    """
    visit - visit another area

    Usage:
      visit
      visit list
        List the areas in this region that you're eligable to visit.

      visit <area name>
        Visit the requested area.
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
        areas = []
        # Get permissions (and returned reasons) for areas
        for area in region.contents:
            if not hasattr(area, 'can_visit'):
                continue
            reason = area.can_visit(character)
            if not reason:
                continue
            areas.append((area, reason))
        if not areas:
            self.msg('{R[There are no areas you can currently visit.]')
            return
        # Sort the list of areas
        areas.sort(key=lambda area: (area[1] != 'Landmark', area[0].key, area[1]))
        # Display the list of areas
        for area, reason in areas:
            if reason == 'Landmark':
                self.msg(area.key)
            else:
                self.msg('{W%s {W(%s{W)' % (area.key, reason))

    def cmd_visit(self):
        character = self.character
        region = character.get_region()
        areas = [area for area in region.contents if hasattr(area, 'can_visit') and area.can_visit(character)]
        results = areas and search_object(self.args, exact=False, candidates=areas) or []
        destination = _AT_SEARCH_RESULT(character, self.args, results, global_search=False, nofound_string="You can't find that area.", multimatch_string="More than one area matches '%s':" % (self.args))
        if not destination:
            return # The search result hook should have informed the user
        # Ensure the player has permission to leave this area
        if character.location:
            if not character.location.access(character, 'leave'):
                # The access check should display a message
                return
        # Ensure the user has enough points to travel
        visit_cost = region.db.region_visit_cost
        if visit_cost:
            for attr, cost in visit_cost:
                if character.game_attribute_current(attr) < cost:
                    self.msg("{R[You need at least %s to visit an area in this region]" % (conj_join([str(cost) + ' ' + attr for attr, cost in visit_cost], 'and')))
                    return
        # Move the character
        if character.containing_room():
            prompt_script = create_script('game.gamesrc.latitude.scripts.prompt_leave.PromptLeave', obj=character, autostart=False)
            prompt_script.db.destination = destination
            prompt_script.db.cost = visit_cost
            prompt_script.db.yes_message = 'You head off in search of your destination.'
            prompt_script.db.no_message = 'You decide to stay where you are.'
            prompt_script.start()
        else:
            message = [character.game_attribute_offset(attr, -cost) for attr, cost in visit_cost]
            self.msg('You head off in search of your destination. %s' % ' '.join(message))
            character.redirectable_move_to(destination)
