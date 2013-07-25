from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import settings, search_object, create_script, utils
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

_AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))

class CmdWander(LatitudeCommand):
    """
    wander - visit a random area

    Usage:
      wander
        Simply leave your current area, and end up somewhere else at random.
        This is the only way to get to certain areas, and some areas will become
        available to the visit command only after you've found them at least once
        by wandering, or being led there by a friend.
    """
    key = "wander"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        character = self.character
        region = character.get_region()
        # Ensure the player has permission to leave this area
        if character.location:
            if not character.location.access(character, 'leave'):
                # The access check should display a message
                return
        # Ensure the user has enough points to travel
        wander_cost = region.db.region_wander_cost
        if wander_cost:
            for attr, cost in wander_cost.iteritems():
                if character.game_attribute_current(attr) < cost:
                    region.at_wander_insufficient(character)
                    self.msg("You're too tired.")
                    return
        # Move the character
        if character.get_room():
            prompt_script = create_script('game.gamesrc.latitude.scripts.prompt_wander.PromptWander', obj=character, autostart=False)
            prompt_script.db.cost = wander_cost
            prompt_script.db.yes_message = 'You set off to explore your surroundings.'
            prompt_script.db.no_message = 'You decide to stay where you are.'
            prompt_script.start()
        else:
            message = ['You set off to explore your surroundings.']
            if wander_cost:
                message.extend([character.game_attribute_offset(attr, -cost) for attr, cost in wander_cost.iteritems()])
            self.msg(' '.join(message))
            region.wander(character)
