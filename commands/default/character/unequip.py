from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdUnequip(LatitudeCommand):
    """
    unequip - Unequip object
    
    Usage:
      unequip <object>
        Attempt to remove a given equipped object.
    """
    key = "unequip"
    aliases = ['doff', 'remove', 'take off']
    locks = "cmd:all()"
    help_category = "Actions"
    arg_regex = r"\s.*?|$"

    def func(self):
        if not self.args:
	    self.msg('Unequip what?')
	    return()
        obj = self.character.search(self.args)
	if not obj:
	    return()
	obj.action_unequip(self.character)
