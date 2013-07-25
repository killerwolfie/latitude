from ev import default_cmds, settings, create_script
from src.objects.models import ObjectDB

class CmdLeave(default_cmds.MuxPlayerCommand):
    """
    leave - Leave your current area.

    Usage:
      leave
        Leave your current area, and return to the region menu.
    """
    key = "leave"
    aliases = []
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"
    help_category = "Actions"

    def func(self):
        character = self.character
        if character.location:
            if not character.location.access(character, 'leave'):
                # The access check should display a message
                return
        # Determine the region
        region = character.get_region()
        if not region and character.home:
            region = character.home.get_region()
        if not region:
            default_home = ObjectDB.objects.get_id(settings.CHARACTER_DEFAULT_HOME)
            region = default_home.get_region()
        if not region:
            raise Exception('could not find region')
        # Create the prompt which will verify with the user, and then do the transporting
        prompt_script = create_script('game.gamesrc.latitude.scripts.prompt_leave.PromptLeave', obj=character, autostart=False)
        prompt_script.db.destination = region
        prompt_script.start()
