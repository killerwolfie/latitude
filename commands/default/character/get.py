from ev import utils, settings, search_object
import re
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

_AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))

class CmdGet(LatitudeCommand):
    """
    get - Pick up an item 

    Usage:
      get [<number> of] <obj> [from <container>]
        Picks up an object (or stack of objects) from your current location.
        Specify <number> to split a stack in your location into your inventory.
        Specify <container> to try to withdraw an item from a container.
    """
    key = "get"
    aliases = ['take']
    locks = "cmd:all()"
    help_category = "Actions"
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.character
        # Sanity check
        if not character.location:
            self.msg("{R[You don't appear to have any specific location to get items from.]")
            return
        # Parse arguments
        target_name = self.args
        quantity = None
        match = re.match(r'(\d+)\s+of\s+(.*)$', target_name)
        if match:
            target_name = match.group(2)
            quantity = int(match.group(1))
        container_name = None
        # Call a special action hook if we're dealing with a withdrawl
        match = re.search(r'(^|.*)\s*from\s+(.+)$', target_name)
        if match:
            target_name = match.group(1).strip() or None
            container_name = match.group(2)
            results = search_object(container_name, exact=False, candidates=[con for con in character.location.contents if con != character])
            container = _AT_SEARCH_RESULT(character, container_name, results, global_search=False)
            if not container:
                return # User is alerted by search hook
            container.action_withdraw(character, target_name)
            return
        # Find object
        if not target_name:
            self.msg('Get what?')
            return
        results = search_object(target_name, exact=False, candidates=[con for con in character.location.contents if con != character])
        target = _AT_SEARCH_RESULT(character, target_name, results, global_search=False)
        if not target:
            return # Search result hook should handle informing the user
        # Check access
        if not target.access(character, 'get'):
            return # Access failure hook should inform the user
        # Do some safety checks to make sure users can't pick up rooms or characters or other silly shit like that
        if not utils.inherits_from(target, 'game.gamesrc.latitude.objects.item.Item'):
            raise Exception('"get" on non-item object')
        if target.bad():
            raise Exception('Interaction with bad object')
        # Verify the quantity
        if utils.inherits_from(target, 'game.gamesrc.latitude.objects.stackable.Stackable'):
            if quantity == None:
                quantity = target.db.quantity
            elif quantity > target.db.quantity:
                self.msg("There aren't enough in that stack.")
                return
            elif quantity < 1:
                self.msg("You need to specify at least one.")
                return
        else:
            if quantity == None:
                quantity = 1
            elif quantity != 1:
                self.msg('You need to pick that up one at a time.')
                return
        # Looks good.  Perform the actual move.
        if utils.inherits_from(target, 'game.gamesrc.latitude.objects.stackable.Stackable'):
            typeclass = target.path
            target.db.quantity -= quantity
            if target.db.quantity <= 0:
                target.delete()
            target = character.give(typeclass, quantity=quantity)[0]
        else:
            target.move_to(character, quiet=True)
        # Alert characters
        if quantity > 1:
            character.msg(character.objsub('You pick up some &1m.', target))
            character.location.msg_contents(character.objsub('&0N picks up some &1m.', target), exclude=character)
        else:
            character.msg(character.objsub('You pick up &1i.', target))
            character.location.msg_contents(character.objsub('&0N picks up &1i.', target), exclude=character)
        # Call hook
        target.at_get(character, quantity=quantity)
