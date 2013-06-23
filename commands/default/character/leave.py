from ev import default_cmds

class CmdLeave(default_cmds.MuxPlayerCommand):
    """
    leave - Leave your current area.

    Usage:
      leave
        Leave with a prompt
      leave now
        Bypass the prompt and leave now
    """
    key = "leave"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        character = self.character
        if self.args.lower() == 'now':
            if character.location:
                if not character.location.access(character, 'leave'):
                    # The access check should display a message
                    return
            # Determine the region object
            region = character.get_region() or character.home.get_region()
            if not region:
                raise Exception('could not find region')
            character.move_to(region)
        elif not self.args:
            character.scripts.add('game.gamesrc.latitude.scripts.prompt_leave.PromptLeave')
        else:
            self.msg('That doesn\'t seem to work.  (See "help leave")')
