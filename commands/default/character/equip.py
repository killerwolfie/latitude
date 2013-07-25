from ev import default_cmds

class CmdEquip(default_cmds.MuxPlayerCommand):
    """
    equip - Equip object
    
    Usage:
      equip <object>
        Attempt to wear a given object
    """

    key = "equip"
    locks = "cmd:all()"
    aliases = ['don', 'put on']
    help_category = "Actions"
    arg_regex = r"\s.*?|$"

    def func(self):
        if not self.args:
	    self.msg('Equip what?')
	    return()
        obj = self.character.search(self.args)
	if not obj:
	    return()
	obj.action_equip(self.character)
