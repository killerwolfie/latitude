"""

Template module for Exits

Copy this module up one level and name it as you like, then
use it as a template to create your own Exits.

To make the default commands (such as @dig/@open) default to creating exits
of your new type, change settings.BASE_EXIT_TYPECLASS to point to
your new class, e.g.

settings.BASE_EXIT_TYPECLASS = "game.gamesrc.objects.myexit.MyExit"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""
from ev import Exit as EvenniaExit
from ev import search_object
from game.gamesrc.latitude.objects.object import Object

class Exit(Object, EvenniaExit):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(Exit, self).basetype_setup()
        self.locks.add(";".join([
            "edit:resident()",            # Allows users to modify this object (required in addition to what is being edited, specifically)
            "edit_appearance:resident()", # Allows users to modify this object's 'appearance' description
            "edit_aura:resident()",       # Allows users to modify this object's 'aura' description
            "edit_flavor:resident()",     # Allows users to modify this object's 'flavor' description
            "edit_scent:resident()",      # Allows users to modify this object's 'scent' description
            "edit_sound:resident()",      # Allows users to modify this object's 'sound' description
            "edit_texture:resident()",    # Allows users to modify this object's 'texture' description
            "edit_writing:resident()",    # Allows users to modify this object's 'writing' description
            "rename:resident()",          # Allows users to rename the object
            "link:resident()",            # Allows users to modify this object's destination (Not the same as 'claiming' the exit, which also changes the destination.)
            "traverse:all()",             # Allows users to pass through the exit
            "traverse_follow:all()",      # Allows users to be carried through the exit
            "get:false()",                # Holding an exit doesn't really make sense
            "drop:false()",               # Dropping an exit doesn't really make sense
            "puppet:false()",             # It would be weird to puppet an exit
            "call:true()",                # Using an exit is done by calling commands on it
        ]))

    def at_object_creation(self):
        self.db.attr_gender = 'Object'

    def return_styled_name(self, looker=None):
        return '{x' + self.key

    def reverse_exits(self):
        """
	Finds the exit on the other side which leads back here.
	"""
	if not self.destination:
	    return None

        if not self.location:
	    return None

	return list(con for con in self.destination.contents if con.destination and con.destination == self.location)

    def at_traverse(self, traversing_object, target_location):
        """
        This implements the actual traversal. The traverse lock has already been
        checked (in the Exit command) at this point.
        """
        if target_location == None:
            # Leaves the 'area'
            traversing_object.scripts.add('game.gamesrc.latitude.scripts.prompt_leave.PromptLeave')
        else:
            super(Exit, self).at_traverse(traversing_object, target_location)

    def at_after_traverse(self, traveller, source_loc):
        # Check for followers
        for follower in search_object(traveller, attribute_name='follow_following'):
            # Ensure that the follower is still at your source location.
            # (Safety check.  Moving around on your own should clear your 'following' attribute)
            if not follower.location or follower.location != source_loc:
                self.at_failed_follow(traveller, follower)
                del follower.db.follow_following
                break
            # Check te ensure that the follower is awake.
            # (Safety check.  Disconnecting your character should clear your 'following' attribute)
            if not follower.player:
                self.at_failed_follow(traveller, follower)
                del follower.db.follow_following
                break
            # Ensure the follower has access to travel through the exit
            if not self.access(follower, 'traverse_follow'):
                self.at_failed_follow(traveller, follower)
                del follower.db.follow_following
                break
            # Bring the follower alonga
            self.at_before_follow(traveller, follower)
            follower.move_to(traveller.location)
            self.at_after_follow(traveller, follower, source_loc)

    def at_before_follow(self, leader, follower):
        """
        Called just before a follower is dragged along after a successful traveller traverses the exit.
        """
        # By default, just call the normal traverse handler
        self.at_before_traverse(follower)

    def at_after_follow(self, leader, follower, source_loc):
        """
        Called just after a follower is dragged along after a successful traveller traverses the exit.
        """
        # By default, just call the normal traverse handler
        self.at_after_traverse(follower, source_loc)
        # And then alert everyone about the follow

    def at_failed_follow(self, leader, follower):
        """
        Called if, for some reason, a follower is unable to successfully be dragged along after a traveller successfully traverses the exit.
        """
        leader.msg('%s seems to have lost you, and is no longer following you.' % follower.key)
        follower.msg('%s moves off, but you find yourself unable to follow.' % leader.key)

    # ---- Object based string substitution ----
    # A - Absolute Pronoun
    def objsub_a(self):
        if self.db.objsub_a:
	    return(str(self.db.objsub_a))
	return("that direction's")

    # O - Objective Pronoun
    def objsub_o(self):
        if self.db.objsub_o:
	    return(str(self.db.objsub_o))
	return('that direction')

    # P - Posessive Pronoun
    def objsub_p(self):
        if self.db.objsub_p:
	    return(str(self.db.objsub_p))
	return("that direction's")

    # R - Reflexive Pronoun
    def objsub_r(self):
        if self.db.objsub_r:
	    return(str(self.db.objsub_r))
	return("that direction")

    # S - Subjective Pronoun
    def objsub_s(self):
        if self.db.objsub_s:
	    return(str(self.db.objsub_s))
	return("that direction")
