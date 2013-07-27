from game.gamesrc.latitude.scripts.script import Script
from ev import managers
from datetime import datetime, timedelta

class MsgPurge(Script):
    def at_script_creation(self):
        self.key = "msg_purge"
        self.desc = "Scans and purges old Msg objects (Pages, channel chatter, etc.)"
        self.interval = 600
        self.persistent = True

    def at_repeat(self):
        start_time = datetime.now()
        # Find all old messages
        old_msgs = managers.msgs.filter(db_date_sent__lt=start_time - timedelta(days=14))
        for old_msg in old_msgs:
            if datetime.now() - start_time >= timedelta(seconds=3):
                # We're taking too long.  Wait until the next run to finish up.
                # FIXME: LOGME
                return
            for channel in old_msg.channels:
                if channel.key in ['MUDconnections', 'MUDinfo']:
                    # These records may be important, so only nuke them by hand
                    return
            if not any(True for receiver in old_msg.receivers if receiver.db.msg_unseen and old_msg in receiver.db.msg_unseen):
                old_msg.delete()
