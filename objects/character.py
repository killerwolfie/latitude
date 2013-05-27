from ev import Character, search_player
from game.gamesrc.latitude.objects.object import LatitudeObject
import time

class LatitudeCharacter(LatitudeObject, Character):
    """
    The Character is like any normal Object (see example/object.py for
    a list of properties and methods), except it actually implements
    some of its hook methods to do some work:

    at_basetype_setup - always assigns the default_cmdset to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_disconnect - stores the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_post_login - retrieves the character's old location and puts it back
                    on the grid with a "charname has connected" message echoed
                    to the room

    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudeCharacter, self).basetype_setup()
        self.permissions = ['Player'] # This is the default permissions that a quelled administrator will want
        self.locks.add(";".join([
            "edit:id(%s)" % (self.dbref),            # Allows users to modify this object (required in addition to what is being edited, specifically)
            "edit_appearance:id(%s)" % (self.dbref), # Allows users to modify this object's 'appearance' description
            "edit_aura:id(%s)" % (self.dbref),       # Allows users to modify this object's 'aura' description
            "edit_flavor:id(%s)" % (self.dbref),     # Allows users to modify this object's 'flavor' description
            "edit_scent:id(%s)" % (self.dbref),      # Allows users to modify this object's 'scent' description
            "edit_sound:id(%s)" % (self.dbref),      # Allows users to modify this object's 'sound' description
            "edit_texture:id(%s)" % (self.dbref),    # Allows users to modify this object's 'texture' description
            "edit_writing:id(%s)" % (self.dbref),    # Allows users to modify this object's 'writing' description
            "edit_gender:id(%s)" % (self.dbref),     # Allows users to modify this object's 'gender' description
            "edit_species:id(%s)" % (self.dbref),    # Allows users to modify this object's 'species' description
            "follow:owner_lock(default_follow)",     # Who can automatically follow
            "lead:owner_lock(default_lead)",         # Who can automatically lead
            "get:false()",                           # Nobody can pick up the character
            "drop:true()",                           # Let's hope this doesn't get called
            "call:false()",                          # No commands can be called on character from outside
        ]))
        # Empty stats
        self.set_attribute('stats_last_unpuppet_time', None)
        self.set_attribute('stats_last_puppet_time', None)

    def at_after_move(self, source_location):
        if self.db.prefs_automap == None or self.db.prefs_automap:
	    self.execute_cmd('map')
        self.execute_cmd('look')

    def at_post_login(self):
        super(LatitudeCharacter, self).at_post_login() # For now call the default handler which unstows the character

    def at_pre_puppet(self, player):
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
	    self.execute_cmd('map')
        self.execute_cmd('look')
        # Alert all your friends :D
        if not self.db.friends_optout:
            for friend in self.player.get_friend_players():
                if friend.shows_online(): # Don't alert friends who show offline.
                    friend.msg('Your friend %s (%s) has just entered the game.' % (self.key, self.player.key))

    def at_post_unpuppet(self, player):
        if self.location:
            self.location.msg_contents("%s has left the game." % self.name, exclude=[self])
        # Update puppet statistics
        self.db.stats_last_unpuppet_time = time.time()

    def shows_online(self):
        """
        Returns whether the character appears to be online.
        This could potentially be used to protect privacy when users request it, but for now it just returns whether they're puppeted.
        """
        return(bool(self.sessid))

    def get_owner(self):
        # Grab the owner name
        owner = self.db.owner
        if not owner:
            return None
        # Grab the owner player object
        owner = search_player(owner)
        if not owner:
            return None
        owner = owner[0]
        # Make sure this character is one of this player's legitimate characters
        if not self in owner.get_playable_characters():
            return None
        # All is well.  Return the player.
        return owner

    # ---- Actions ----
    def action_stop(self, stopper):
        if self == stopper:
            # Stopping yourself.  Stop following
            leader = self.db.follow_following
            # Ensure we're ready to clear the follow
            if not leader:
                self.msg("You're not currently following anyone.")
                return
            # Clear the follow
            del self.db.follow_following
            self.msg(self.objsub('You stop following &1n.', leader))
            leader.msg(self.objsub('&0N stops following you.', leader))
        else:
            # Stopping someone else.  Stop leading.
            if not self.db.follow_following == stopper:
                stopper.msg(self.objsub("&0N isn't following you.", stopper))
                return
            del self.db.follow_following
            stopper.msg(self.objsub('You stop leading &0n.', stopper))
            self.msg(self.objsub('&1n stops leading you.', stopper))

