"""

Template for Objects

Copy this module up one level and name it as you like, then
use it as a template to create your own Objects.

To make the default commands default to creating objects of your new
type (and also change the "fallback" object used when typeclass
creation fails), change settings.BASE_OBJECT_TYPECLASS to point to
your new class, e.g.

settings.BASE_OBJECT_TYPECLASS = "game.gamesrc.objects.myobj.MyObj"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""
from ev import Object
from ev import Exit
from ev import Room

class LatitudeObject(Object):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     aliases (list of strings) - aliases to the object. Will be saved to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     dbobj (Object, read-only) - link to database model. dbobj.typeclass points back to this class
     typeclass (Object, read-only) - this links back to this class as an identified only. Use self.swap_typeclass() to switch.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     player (Player) - controlling player (will also return offline player)
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     sessions (list of Sessions, read-only) - returns all sessions connected to this object
     has_player (bool, read-only)- will only return *connected* players
     contents (list of Objects, read-only) - returns all objects inside this object (including exits)
     exits (list of Objects, read-only) - returns all exits from this object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None, use_nicks=False, location=None, ignore_errors=False, player=False)
     execute_cmd(raw_string)
     msg(message, from_obj=None, data=None)
     msg_contents(message, exclude=None, from_obj=None, data=None)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so their arguments should also start with self):

     basetype_setup()     - only called once, used for behind-the-scenes setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created. Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning False, deletion is aborted. Note that all objects
                          inside a deleted object are automatically moved to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory, at least once every server restart/reload
     at_cmdset_get()      - this is called just before the command handler requests a cmdset from this object
     at_first_login()     - (player-controlled objects only) called once, the very first time user logs in.
     at_pre_login()       - (player-controlled objects only) called every time the user connects, after they have identified, before other setup
     at_post_login()      - (player-controlled objects only) called at the end of login, just before setting the player loose in the world.
     at_disconnect()      - (player-controlled objects only) called just before the user disconnects (or goes linkless)
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_before_move(destination)             - called just before moving object to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just after move, if obj.move_to() has quiet=False
     at_after_move(source_location)          - always called after a move has been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives another object

     at_before_traverse(traversing_object)                 - (exit-objects only) called just before an object traverses this object
     at_after_traverse(traversing_object, source_location) - (exit-objects only) called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, data=None) - called when a message (via self.msg()) is sent to this obj.
                                                           If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, data=None) - called when this objects sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look" command by default
     at_desc(looker=None)      - called by 'look' whenever the appearance is requested.
     at_get(getter)            - called after object has been picked up. Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this object speaks

    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudeObject, self).basetype_setup()
        # Clear the locks assigned by the built in Evennia base class
        self.locks.replace("")
        # Add some administrative locks.  These are used to control access to sensitive privilidged operations.
        # The locks control whether a user can even attempt to perform an action on the object, so the same locks are defined for all objects even if they only apply to certain types of objects.
        self.locks.add(";".join([
            "admin_alias:pperm(Janitors)",     # Permits the use of administrative commands to modify the object's aliases
            "admin_examine:pperm(Janitors)",   # Permits the use of administrative commands to examine the object and its properties
            "admin_delete:pperm(Janitors)",    # Permits the use of administrative commands to delete the object
            "admin_tel:pperm(Janitors)",       # Permits the use of administrative commands to teleport the object to other locations
            "admin_telto:pperm(Janitors)",     # Permits the use of administrative commands to teleport objects into this object
            "admin_set:pperm(Janitors)",       # Permits the use of administrative commands to set properties on the object
            "admin_rename:pperm(Janitors)",    # Permits the use of administrative commands to rename the object
            "admin_link:pperm(Janitors)",      # Permits the use of administrative commands to set the destination of this object
            "admin_typeclass:pperm(Janitors)", # Permits the use of administrative commands to change the typeclass of this object
            "admin_perm:pperm(Janitors)",      # Permits the use of administrative commands to set 'permissions' on this object
            "admin_lock:pperm(Janitors)",      # Permits the use of administrative commands to change locks on this object
            "admin_script:pperm(Janitors)",    # Permits the use of administrative commands to attach scripts to this object
        ]))
        # Set the default permissions which apply to all objects.
        # This is sparse because the base object class is not intended to be used directly for objects in the world.
        self.locks.add(";".join([
            "call:false()",                  # allow to call commands on this object (Used by the system itself)
            "puppet:id(%s) or pperm(Janitors)" % self.dbref,
        ])) # restricts puppeting of this object

    # ----- Lock Messages -----
    def at_access_failure(self, accessing_obj, access_type):
        # Check for a custom message property
        if self.db.access_failure and access_type in self.db.access_failure:
            if self.db.access_failure[access_type] != None:
                accessing_obj.msg(self.db.access_failure[access_type])
            return
        # Ignore access types used directly by the Evennia engine
        if access_type == 'call':
            return
        # Otherwise, create a default message
        message_table = {
            'get' : "{RYou can't pick that up",
            'drop' : "{RYou can't drop that",
            'rename' : "{RYou can't rename that object",
            'edit' : "{RYou can't edit that object",
            'edit_gender' : "{RYou can't edit the {rgender{R of that object",
            'edit_appearance' : "{RYou can't edit the {rappearance{R of that object",
            'edit_aura' : "{RYou can't edit the {raura{R of that object",
            'edit_flavor' : "{RYou can't edit the {rflavor{R of that object",
            'edit_scent' : "{RYou can't edit the {rscent{R of that object",
            'edit_sound' : "{RYou can't edit the {rsound{R of that object",
            'edit_texture' : "{RYou can't edit the {rtexture{R of that object",
            'edit_writing' : "{RYou can't edit the {rwriting{R on that object",
        }
        if access_type in message_table:
            message = message_table[access_type]
        else:
            message = '{RAccess denied ({r%s{R)' % (access_type)
        accessing_obj.msg('{R[ %s{R ]' % message)

    def at_access_success(self, accessing_obj, access_type):
        # Check for a message property (sending nothing by default)
        if self.db.access_failure and access_type in self.db.access_failure and self.db.access_failure[access_type] != None:
            accessing_obj.msg(self.db.access_failure[access_type])

    # ----- Descriptions -----
    def return_appearance(self, looker):
        """
        Describes the appearance of this object.  Used by the "look" command.
	This method, by default, delegates its desc generation into several other calls on the object.
	   return_appearance_name for the name of the object. (Which defaults to showing nothing)
	   return_apperaance_desc to generate the main description of the room.
           return_appearance_exits to generate a line that shows you which exits are available for you to take
	   return_appearance_contents to generate the description of the contents of the object
	      (This, itself, calls return_appearance_contents_header if there are any contents to get the 'Carrying:' line by default)
	"""
        if not looker:
            return()

	descs = [self.return_appearance_name(looker), self.return_appearance_desc(looker), self.return_appearance_exits(looker), self.return_appearance_contents(looker)]
	descs = [desc for desc in descs if desc != None]
	return('\n'.join(descs))

    def return_appearance_name(self, looker):
        """
	Return the name portion of the visual description.
	By default, the name of the object is not announced when getting the description.
	"""
        return(None)

    def return_appearance_desc(self, looker):
        """
	Return the main portion of the visual description.
	"""
        desc = self.db.desc_appearance
	if desc != None:
	    return('%cn' + desc)
	else:
	    return('%cnYou see nothing special.')

    def return_appearance_exits(self, looker):
        """
	Return a line that describes the visible exits in the object.
	"""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker)
        exits = []
        for con in visible:
            if isinstance(con, Exit):
                exits.append(con.key)

        if exits:
            return('%ch%cx[Exits: ' + ', '.join(exits) + ']%cn')
	else:
	    return(None)

    def return_appearance_contents(self, looker):
        """
	Return a descriptive list of the contents held by this object.
	"""
        visible = (con for con in self.contents if con != looker)
        exits, users, things = [], [], []
        for con in visible:
            key = con.key
            if isinstance(con, Exit):
	        exits.append(con.key)
            elif con.player:
                users.append("{c%s{n" % key)
            else:
                things.append(key)
        if users or things:
            string = self.return_appearance_contents_header(looker)
            if users:
                string += '\n%ch%cc' + '\n'.join(users) + '%cn'
            if things:
                string += '\n%cn%cc' + '\n'.join(things) + '%cn'
            return(string)
	else:
	    return(None)

    def return_appearance_contents_header(self, looker):
        """
	Returns a header line to display just before outputting the contents of the object.
	"""
        return('%ch%cbContents:%cn')

    def return_scent(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_scent:
	    return self.db.desc_scent
	else:
	    return self.return_situational_name().capitalize() + " doesn't seem to have any descernable scent."

    def return_texture(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_texture:
	    return self.db.desc_texture
	else:
	    return self.return_situational_name().capitalize() + " doesn't seem to have any descernable texture."

    def return_flavor(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_flavor:
	    return self.db.desc_flavor
	else:
	    return self.return_situational_name().capitalize() + " doesn't seem to have any descernable flavor."

    def return_sound(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_sound:
	    return self.db.desc_sound
	else:
	    return self.return_situational_name().capitalize() + " doesn't seem to have any descernable sound."

    def return_aura(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_aura:
	    return self.db.desc_aura
	else:
	    return self.return_situational_name().capitalize() + " doesn't seem to have any descernable aura."

    def return_writing(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_writing:
	    return self.db.desc_writing
	else:
	    return self.return_situational_name().capitalize() + " doesn't seem to have any descernable writing."

    def return_situational_name(self):
        """
        A situational name is used by alerts that are sent to other players.
        In almost all cases, a character's name should be their situational name, but for objects it's often not.
        Examples:
            Object: 'Water Fountain' would return 'the water fountain'
            Exit: '[E]astern Gate' would return 'the eastern gate'
            Room: Most rooms would return 'this room'
        """
        if self.db.desc_situational_name:
            return self.db.desc_situational_name
        return self.key

    # ----- Maps -----
    def return_map(self, mark_friends_of=None):
        """
	Return an ascii image representing the location of the object for helping users to navigate.
	"""
	room = self.containing_room()
	if hasattr(room, 'return_map'):
	    return room.return_map(mark_friends_of)
	return None

    # ----- Pronoun Substitution -----
    def return_pronoun_reflexive(self):
        if self.db.desc_pronoun_reflexive:
	    return(self.db.desc_pronoun_reflexive)
	if self.is_male():
	    return('himself')
	if self.is_female():
	    return('herself')
        if self.is_herm():
	    return('hirself')
	if self.is_neuter():
	    return('itself')
	return(self.key)

    def return_pronoun_posessive(self):
        if self.db.desc_pronoun_posessive:
	    return(self.db.desc_pronoun_posessive)
	if self.is_male():
	    return('his')
	if self.is_female():
	    return('her')
        if self.is_herm():
	    return('hir')
	if self.is_neuter():
	    return('its')
	return(self.key + "'s")

    def return_pronoun_objective(self):
        if self.db.desc_pronoun_objective:
	    return(self.db.desc_pronoun_objective)
	if self.is_male():
	    return('him')
	if self.is_female():
	    return('her')
        if self.is_herm():
	    return('hir')
	if self.is_neuter():
	    return('it')
	return(self.key)

    def return_pronoun_subjective(self):
        if self.db.desc_pronoun_subjective:
	    return(self.db.desc_pronoun_subjective)
	if self.is_male():
	    return('he')
	if self.is_female():
	    return('she')
        if self.is_herm():
	    return('shi')
	if self.is_neuter():
	    return('it')
	return(self.key)

    def return_pronoun_absolute(self):
        if self.db.desc_pronoun_absolute:
	    return(self.db.desc_pronoun_absolute)
	if self.is_male():
	    return('his')
	if self.is_female():
	    return('hers')
        if self.is_herm():
	    return('hirs')
	if self.is_neuter():
	    return('its')
	return(self.key + "'s")

    # ----- Gender -----
    def is_male(self):
        if self.db.attr_gender:
            return(self.db.attr_gender.lower().rstrip() in ['male', 'man', 'boy', 'dude', 'him'])
        return False

    def is_female(self):
        if self.db.attr_gender:
            return(self.db.attr_gender.lower().rstrip() in ['female', 'woman', 'girl', 'chick', 'her'])
        return False

    def is_herm(self):
        if self.db.attr_gender:
            return(self.db.attr_gender.lower().rstrip() in ['herm', 'hermy', 'both', 'shemale'])
        return False

    def is_neuter(self):
        if self.db.attr_gender:
            return(self.db.attr_gender.lower().rstrip() in ['neuter', 'asexual', 'it', 'thing', 'object', 'machine'])
        return False

    # ----- Event Hooks -----
    def at_desc(self, looker):
        pass

    def at_desc_scent(self, looker):
        pass

    def at_desc_flavor(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg('%s just smelled you!' % (looker.key))
        if looker.location:
            looker.location.msg_contents('%s just smelled %s.' % (looker.key, self.return_situational_name()))

    def at_desc_texture(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg('%s just smelled you!' % (looker.key))
        if looker.location:
            looker.location.msg_contents('%s just smelled %s.' % (looker.key, self.return_situational_name()))

    def at_desc_sound(self, looker):
        pass

    def at_desc_aura(self, looker):
        pass

    def at_desc_writing(self, looker):
        pass

    # ----- Player Actions -----
    def action_use(self, user):
        """
        Called when a player attempts to use this object, without using it on something specific.
        This allows the object to decide its default target, if it's targetable.
        """
        user.msg("You can't use that.")

    def action_use_on(self, user, targets):
        """
        Called when a player attempts to use this object on another object.
        It also works on multiple objects, for example: use vacuum cleaner on dust bunny, crumbs
        """
        # If there's only one target, then the default is to try reversing it.
        if len(targets) == 1:
            targets[0].action_used_on_by(user, self)
        else:
            user.msg("That doesn't work.")

    def action_used_on_by(self, user, targets):
        """
        This is a secondary call, when the system is unable or unwilling to call 'use_on' for an object.
        It's called to indicate that a player wants to use an object on this object.
        It also works with multiple objects, for example: use candy wrapper, pop can on trash bin
        """
        user.msg("That doesn't work.")

    def action_lock(self, locker):
        """
        This action is called when a player attempts to 'lock' the object.
        The definition of locking is left up to the object creator.
        """
        locker.msg("You can't lock that!")

    def action_unlock(self, unlocker):
        """
        This action is called when a player attempts to 'lock' the object.
        The definition of locking is left up to the object creator.
        """
        unlocker.msg("You can't unlock that!")

    # ----- Utilities -----
    def containing_room(self):
        """
	Ascends the tree until it hits the first room, and returns it.
	"""
        obj_seen = set([self])
        room = self.location
        while room:
            if room in obj_seen:
                raise Exception('Object loop detected!  ' + room.dbref + ' contains itself!')
            obj_seen.add(room)
            if isinstance(room.typeclass, Room):
                break
            room = room.location
	if room and room.location != None:
	    raise Exception('"Child" room detected!  ' + room.dbref + ' has a location!')
        return room

    def is_inside(self, obj):
        """
	Ascends the tree to determine if this object is inside obj
	"""
        obj_seen = set([self])
        parent = self.location
        while parent:
            if parent in obj_seen:
                raise Exception('Object loop detected!  ' + parent.dbref + ' contains itself!')
            obj_seen.add(parent)
	    if parent == obj:
	        return True
            parent = parent.location
	return False

    # ----- Default Behavior -----
    def at_after_move(source_location):
        super(LatitudeObject, self).at_after_move(source_location)
        # Clear 'following'
        following = self.db.follow_following
        if following and following.location == None or following.location != self.location:
            self.msg('You move off, and stop following %s.' % (following.key))
            del self.db.follow_following
        # Clear any pending follow or lead requests
        del self.db.follow_wantfollow
        del self.db.follow_wantlead
