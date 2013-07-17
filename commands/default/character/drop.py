from ev import default_cmds, utils, settings, search_object
import re

_AT_SEARCH_RESULT = utils.variable_from_module(*settings.SEARCH_AT_RESULT.rsplit('.', 1))

class CmdDrop(default_cmds.MuxPlayerCommand):
    """
    drop - Leave an item at your current location

    Usage:
      drop <obj>
        Drop an object from your inventory

      drop <num> of <obj>
        Drops a specific number from a stack of objects in your inventory.
    """

    key = "drop"
    arg_regex = r"\s.*?|$"
    locks = "cmd:all()"
    help_category = "Actions"

    def func(self):
        character = self.character
        # Sanity check
        if not character.location:
            self.msg("{R[You don't appear to have any specific location to drop items into.]")
            return
        # Parse arguments
        target_name = self.args
        quantity = None
        match = re.match(r'(\d)+\s+of\s+(.*)$', target_name)
        if match:
            target_name = match.group(2)
            quantity = int(match.group(1))
        if not target_name:
            self.msg('Get what?')
            return
        # Find object
        results = search_object(target_name, exact=False, candidates=character.contents)
        target = _AT_SEARCH_RESULT(character, target_name, results, global_search=False)
        if not target:
            return # Search result hook should handle informing the user
        if not target.access(character, 'get'):
            return # Access failure hook should inform the user
        # Do some safety checks in case somehow a user manages to target some room or character or something bizzare
        if not utils.inherits_from(target, 'game.gamesrc.latitude.objects.item.Item'):
            raise Exception('"drop" on non-item object')
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
            target = character.location.give(typeclass, quantity=quantity)[0]
        else:
            target.move_to(character.location, quiet=True)
        # Alert characters
        if quantity > 1:
            character.msg(character.objsub('You drop some &1m.', target))
            character.location.msg_contents(character.objsub('&0N drops some &1m.', target), exclude=character)
        else:
            character.msg(character.objsub('You drop &1i.', target))
            character.location.msg_contents(character.objsub('&0N drops &1i.', target), exclude=character)
        # Call hook
        target.at_drop(character, quantity=quantity)
