from game.gamesrc.latitude.scripts.prompt_state import PromptState

class PromptWander(PromptState):
    """
    Prompt the user if they want to go, before moving them to their destination.

    Attributes:
        cost - A list of pairs: attribute, and cost, if the user accepts the move.
               Any checks for sufficient attributes should be made before creating the
               script.
        yes_message - A message to display to the user if they choose to wander.
        no_message - A message to display to the user if they choose to not wander.
    """
    def prompt_options(self):
        self.obj.msg('Are you sure you want to leave the area? (y/n)')

    def prompt_option_y(self):
        self.ndb.user_picked_yes = True
        return None

    def prompt_option_n(self):
        self.ndb.user_picked_yes = False
        return None

    def prompt_end(self):
        if self.ndb.user_picked_yes:
            region = self.obj.get_region()
            message = [self.db.yes_message or 'You set off to explore your surroundings.']
            if self.db.cost:
                message.extend([self.obj.game_attribute_offset(attr, -cost) for attr, cost in self.db.cost])
            self.obj.msg(' '.join(message))
            region.wander(self.obj.typeclass) # FIXME: Upstream issue 399
        else:
            self.obj.msg(self.db.no_message or 'You decide to stay where you are.')
