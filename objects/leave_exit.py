from game.gamesrc.latitude.objects.exit import Exit
from ev import create_script

class LeaveExit(Exit):
    def at_traverse(self, traversing_object, target_location):
        prompt_script = create_script('game.gamesrc.latitude.scripts.prompt_leave.PromptLeave', obj=traversing_object, autostart=False)
        prompt_script.db.destination = self.get_region()
        prompt_script.start()
