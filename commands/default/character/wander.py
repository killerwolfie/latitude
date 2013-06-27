from game.gamesrc.latitude.utils.stringmanip import conj_join
from ev import default_cmds, settings, search_object, create_script, utils

_AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))

class CmdWander(default_cmds.MuxPlayerCommand):
    """
    wander - visit a random area
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
            for attr, cost in wander_cost:
                if character.game_attribute_current(attr) < cost:
                    self.msg("{R[You need at least %s to explore this area.]" % (conj_join([str(cost) + ' ' + attr for attr, cost in wander_cost], 'and')))
                    return
        # Move the character
        if character.containing_room():
            prompt_script = create_script('game.gamesrc.latitude.scripts.prompt_wander.PromptWander', obj=character, autostart=False)
            prompt_script.db.cost = wander_cost
            prompt_script.db.yes_message = 'You set off to explore your surroundings.'
            prompt_script.db.no_message = 'You decide to stay where you are.'
            prompt_script.start()
        else:
            message = ['You set off to explore your surroundings.']
            if wander_cost:
                message.extend([character.game_attribute_offset(attr, -cost) for attr, cost in wander_cost])
            self.msg(' '.join(message))
            region.wander(character)
