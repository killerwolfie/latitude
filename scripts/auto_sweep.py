from game.gamesrc.latitude.scripts.script import Script
from ev import search_object, managers, utils
import time

class AutoSweep(Script):
    def at_script_creation(self):
        self.key = "auto_sweep"
        self.desc = "Automatically moves sleeping characters"
        self.interval = 30
        self.persistent = True

    def at_repeat(self):
        now = time.time()
        for room in [obj for obj in ev.managers.objects.get_objs_with_attr('autosweep_active') if hasattr(obj, 'autosweep')]:
            room.autosweep()
