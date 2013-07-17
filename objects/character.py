from ev import search_player, search_object, utils
from ev import Character as EvenniaCharacter
from src.scripts.models import ScriptDB
from game.gamesrc.latitude.objects.actor import Actor
import time

class Character(Actor, EvenniaCharacter):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(Character, self).basetype_setup()
        self.permissions = ['Player'] # This is the default permissions that a quelled administrator will want
        self.locks.add(";".join([
            "char_delete:owner() or perm(Janitor)", # Allows users to delete this object with the @char command.
            "rename:owner()",                       # Allows users to rename this object
            "edit:owner()",                         # Allows users to modify this object (required in addition to what is being edited, specifically)
            "edit_appearance:owner()",              # Allows users to modify this object's 'appearance' description
            "edit_aura:owner()",                    # Allows users to modify this object's 'aura' description
            "edit_flavor:owner()",                  # Allows users to modify this object's 'flavor' description
            "edit_scent:owner()",                   # Allows users to modify this object's 'scent' description
            "edit_sound:owner()",                   # Allows users to modify this object's 'sound' description
            "edit_texture:owner()",                 # Allows users to modify this object's 'texture' description
            "edit_writing:owner()",                 # Allows users to modify this object's 'writing' description
            "edit_gender:owner()",                  # Allows users to modify this object's 'gender' description
            "edit_species:owner()",                 # Allows users to modify this object's 'species' description
            "view_contents:self()",                 # Allows users to view the contents of this object
            "follow:owner_lock(default_follow)",    # Who can automatically follow
            "lead:owner_lock(default_lead)",        # Who can automatically lead
            "get:false()",                          # Nobody can pick up the character
            "drop:true()",                          # Let's hope this doesn't get called
            "call:false()",                         # No commands can be called on character from outside
        ]))
        # Empty stats
        self.set_attribute('stats_last_unpuppet_time', None)
        self.set_attribute('stats_last_puppet_time', None)

    def bad(self):
        """
        Audits whether the object is corrupted in some way, such as being a duplicate
        character name.

        If the character is valid, then None is returned.  If it's broken, then a
        string is returned containing a reason why.
        """
        # Owner security check
        if self.db.owner and not self.get_owner():
            return 'owner security check failed'
        # Looks like we're good.
        return super(Character, self).bad()

    def at_post_login(self):
        super(Character, self).at_post_login() # For now call the default handler which unstows the character

    def at_pre_puppet(self, player, sessid):
        if self.location:
            self.location.msg_contents("%s has entered the game." % self.name, exclude=[self])
        # Update puppet statistics
        self.db.stats_last_puppet_time = time.time()
        self.db.stats_last_puppet_player = player
        if self.db.stats_times_puppeted:
            self.db.stats_times_puppeted += 1
        else:
            self.db.stats_times_puppeted = 1

    def at_post_puppet(self):
        if self.db.prefs_automap == None or self.db.prefs_automap:
	    self.execute_cmd('map', sessid=self.sessid)
        self.execute_cmd('look', sessid=self.sessid)
        # Alert all your friends :D
        if not self.db.friends_optout:
            for friend in self.player.get_friend_players():
                if friend.status_online(): # Don't alert friends who show offline.
                    friend.msg('{Y[Your friend %s{Y (%s{Y) has just entered the game.]' % (self.key, self.player.key))

    def at_post_unpuppet(self, player, sessid):
        if self.location:
            self.location.msg_contents("%s has left the game." % self.name, exclude=[self])
        # Update puppet statistics
        self.db.stats_last_unpuppet_time = time.time()

    def set_owner(self, new_owner):
        # Remove current owner
        owner = self.get_owner()
        if owner:
            if self in owner.db.characters:
                owner.db.characters.remove(self)
            self.db.owner = None
        # Set the new owner
        if new_owner:
            if not new_owner.db.characters:
                new_owner.db.characters = set()
            new_owner.db.characters.add(self)
            self.db.owner = new_owner

    def get_owner(self):
        # Do some security checks to prevent messed up characters from having an official owner
        owner = self.db.owner
        if not owner:
            return None
        # Verify that the player data also shows ownership
        if not self in owner.db.characters:
            return None
        # Verify that, among character objects, this one has a unique name
        if len([char for char in search_object(self.key, attribute_name='key') if isinstance(char, Character)]) != 1:
            return None
        # Verify this doesn't match the name of any player, unless that player is our own
        if self.key.lower() != owner.key.lower() and search_player(self.key):
            return None
        # Looks good, return the owner.
        return self.db.owner

    def status_online(self):
        """
        Returns whether the character appears to be online.
        This could potentially be used to protect privacy when users request it, but for now it just returns whether they're puppeted.
        """
        if self.sessid:
            return time.time() - self.player.get_session(sessid=self.sessid).conn_time
        else:
            return None

    def status_idle(self):
        """
        Returns the idle time of the character, in seconds.

        Returns None if the character is offline.
        """
        if self.status_online():
            return time.time() - self.player.get_session(sessid=self.sessid).cmd_last_visible
        else:
            return None

    # ---- Descriptions ----
    def get_desc_styled_name(self, looker=None):
        if self.status_online():
            return '{c' + self.key
        else:
            return '{C' + self.key

    # ----- Object based string substitution -----

    # D - Definite Name
    def objsub_d(self):
        return self.key

    # I - Indefinite Name
    def objsub_i(self):
        return self.key
