from game.gamesrc.latitude.scripts.script import Script
from game.gamesrc.latitude.utils.log import *
from ev import managers
from django.db.models import Max

class Audit(Script):
    def at_script_creation(self):
        self.key = "audit"
        self.desc = "Scans for bad objects and players"
        self.interval = 5
        self.persistent = True

    def at_repeat(self):
        self.run_audit(30)

    def run_audit(self, num_objs=None):
        if self.db.audit_known_bad == None:
            self.db.audit_known_bad = set()
        # Objects
        if num_objs:
            obj_start = (self.db.audit_last_object or 0) + 1
            obj_end = obj_start + max(num_objs / 3, 1)
        else:
            obj_start = None
            obj_end = None
        objs = managers.objects.get_dbref_range(obj_start, obj_end)
        for obj in sorted(objs, key=lambda obj: obj.id):
            self.audit(obj)
        if obj_end:
            if obj_end <= managers.objects.aggregate(Max('id'))['id__max']:
                self.db.audit_last_object = obj_end
            else:
                # We cycled through.  Restart next time
                del self.db.audit_last_object
        # Players
        if num_objs:
            player_start = (self.db.audit_last_player or 0) + 1
            player_end = player_start + max(num_objs / 3, 1)
        else:
            player_start = None
            player_end = None
        players = managers.players.get_dbref_range(player_start, player_end)
        for player in sorted(players, key=lambda player: player.id):
            self.audit(player)
        if player_end:
            if player_end <= managers.players.aggregate(Max('id'))['id__max']:
                self.db.audit_last_player = player_end
            else:
                # We cycled through.  Restart next time
                del self.db.audit_last_player
        # Scripts
        if num_objs:
            script_start = (self.db.audit_last_script or 0) + 1
            script_end = script_start + max(num_objs / 3, 1)
        else:
            script_start = None
            script_end = None
        scripts = managers.scripts.get_dbref_range(script_start, script_end)
        for script in sorted(scripts, key=lambda script: script.id):
            self.audit(script)
        if script_end:
            if script_end <= managers.scripts.aggregate(Max('id'))['id__max']:
                self.db.audit_last_script = script_end
            else:
                # We cycled through.  Restart next time
                del self.db.audit_last_script

    def audit(self, obj):
        if hasattr(obj, 'bad'):
            # Perform the check
            try:
                result = obj.bad()
            except Exception as e:
                result = 'exception raised during audit (%s)' % (e)
            # Handle the results
            if result:
                # An error was returned
                if not obj in self.db.audit_known_bad:
                    log_info('[Audit] "%s" %s(%s) %r' % (result, obj.key, obj.dbref, obj))
                    self.db.audit_known_bad.add(obj)
            else:
                # All was well
                if obj in self.db.audit_known_bad:
                    self.db.audit_known_bad.remove(obj)
