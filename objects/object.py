from ev import Object
from ev import Exit
from ev import Room
import re

class LatitudeObject(Object):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudeObject, self).basetype_setup()
        # Clear the locks assigned by the built in Evennia base class
        self.locks.replace("")
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
            'follow' : None, # Follow system handles this by sending a follow request.
            'lead' : None, # Follow system handles this by sending a lead request.
        }
        if access_type in message_table:
            message = message_table[access_type]
        else:
            message = '{RAccess denied ({r%s{R)' % (access_type)
        if message:
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
	    return self.objsub("&0C doesn't seem to have any descernable scent.")

    def return_texture(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_texture:
	    return self.db.desc_texture
	else:
	    return self.objsub("&0C doesn't seem to have any descernable texture.")

    def return_flavor(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_flavor:
	    return self.db.desc_flavor
	else:
	    return self.objsub("&0C doesn't seem to have any descernable flavor.")

    def return_sound(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_sound:
	    return self.db.desc_sound
	else:
	    return self.objsub("&0C doesn't seem to have any descernable sound.")

    def return_aura(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_aura:
	    return self.db.desc_aura
	else:
	    return self.objsub("&0C doesn't seem to have any descernable aura.")

    def return_writing(self, looker):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_writing:
	    return self.db.desc_writing
	else:
	    return self.objsub("&0C doesn't seem to have any descernable writing.")

    # ----- Maps -----
    def return_map(self, mark_friends_of=None):
        """
	Return an ascii image representing the location of the object for helping users to navigate.
	"""
	room = self.containing_room()
	if hasattr(room, 'return_map'):
	    return room.return_map(mark_friends_of)
	return None
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
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg(self.objsub('&1N just smelled you!', looker))
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just smelled &0c.', looker), exclude=[self, looker])

    def at_desc_flavor(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg(self.objsub('&1N just tasted you!', looker))
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just tasted &0c.', looker), exclude=[self, looker])

    def at_desc_texture(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg(self.objsub('&1N just felt you!', looker))
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just felt &0c.', looker), exclude=[self, looker])

    def at_desc_sound(self, looker):
        pass

    def at_desc_aura(self, looker):
        pass

    def at_desc_writing(self, looker):
        pass

    def at_say(self, speaker, message):
        pass

    def at_whisper(self, speaker, message):
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

    def action_stop(self, stopper):
        """
        This action is called when a player attempts to 'stop' the object.
        """
        stopper.msg("You can't stop that.")

    def action_start(self, starter):
        """
        This action is called when a player attempts to 'start' the object
        """
        starter.msg("You can't start that.")

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

    # ----- Object based string substitution -----
    def objsub(self, template, *args):
        def repl(codeseq):
            # Determine which object we're asking for a substitution
            objnum = int(codeseq.group(1))
            if objnum == 0:
                subobj = self
            elif objnum <= len(args):
                subobj = args[objnum - 1]
            else:
                return(codeseq.group(0))
            # Determine whether we're capitalizing or not
            if codeseq.group(2).isupper():
                capitalize = True
                code = codeseq.group(2).lower()
            else:
                capitalize = False
                code = codeseq.group(2)
            # Determine what to substitute, and get the substitution
            if hasattr(subobj, 'objsub_' + code):
                retval = getattr(subobj, 'objsub_' + code)()
            else:
                retval = subobj.objsub_other(code)
            # If the function returns 'None' then we want to ignore this substitution
            if retval == None:
                return codeseq.group(0)
            # Capitalize if necessary, and return the value.
            if capitalize:
                retval = retval[0].upper() + retval[1:]
            return retval
        return re.sub(r'&([0-9])([a-zA-Z])', repl, template)
    
    # A - Absolute Pronoun
    def objsub_a(self):
        if self.db.objsub_a:
	    return(str(self.db.objsub_a))
	if self.is_male():
	    return('his')
	if self.is_female():
	    return('hers')
        if self.is_herm():
	    return('hirs')
	if self.is_neuter():
	    return('its')
	return(self.key + "'s")

    # C - Casual Name
    def objsub_c(self):
        """
        The casual name is used to order to casually refer to the object.

        Examples:
            Object: 'Water Fountain' would return 'the water fountain'
            Exit: '[E]astern Gate' would return 'the eastern gate'
            Room: Most rooms would return 'this room'

        In almost all cases, a character's name should be their casual name, but for objects it's often not.
        """
        if self.db.objsub_c:
	    return(str(self.db.objsub_c))
        return self.key

    # N - Object Name
    def objsub_n(self):
        """
        This is the proper name of the object.
        Even though it's possible to override this, it would probably be bad, because it's used to identify the object to other players.
        It would allow a character to masquerade as another character, for example.  Not good.
        """
        if self.db.objsub_n:
	    return(str(self.db.objsub_n))
        return self.key

    # O - Objective Pronoun
    def objsub_o(self):
        if self.db.objsub_o:
	    return(str(self.db.objsub_o))
	if self.is_male():
	    return('him')
	if self.is_female():
	    return('her')
        if self.is_herm():
	    return('hir')
	if self.is_neuter():
	    return('it')
	return(self.key)

    # P - Posessive Pronoun
    def objsub_p(self):
        if self.db.objsub_p:
	    return(str(self.db.objsub_p))
	if self.is_male():
	    return('his')
	if self.is_female():
	    return('her')
        if self.is_herm():
	    return('hir')
	if self.is_neuter():
	    return('its')
	return(self.key + "'s")

    # R - Reflexive Pronoun
    def objsub_r(self):
        if self.db.objsub_r:
	    return(str(self.db.objsub_r))
	if self.is_male():
	    return('himself')
	if self.is_female():
	    return('herself')
        if self.is_herm():
	    return('hirself')
	if self.is_neuter():
	    return('itself')
	return(self.key)

    # S - Subjective Pronoun
    def objsub_s(self):
        if self.db.objsub_s:
	    return(str(self.db.objsub_s))
	if self.is_male():
	    return('he')
	if self.is_female():
	    return('she')
        if self.is_herm():
	    return('shi')
	if self.is_neuter():
	    return('it')
	return(self.key)

    # W - Within Name
    def objsub_w(self):
        """
        The within name describes the state of being within the object.

        Examples:
            Character/NPC: in Ted's pocket
            Room: at the southern doors
            Areas: in the Pleasantville Shopping Mall <-- Technically not an object, but also has within names
            Regions: on the moon <-- Technically not an object, but also has within names

        This can be used to generate a sentence (Combined with the casual name):
            That's a pencil, in Ted's pocket, at the southern doors, in the Pleasantville Shopping Mall, on the moon.
        """
        if self.db.objsub_w:
	    return(str(self.db.objsub_w))
        return 'in ' + self.key

    # Other
    def objsub_other(self, code):
        # Since untrusted strings generate calls to this function, be rigorous about what to accept.
        if not isinstance(code, basestring):
            raise TypeError
        if not len(code) == 1:
            raise ValueError
        if not code.islower():
            raise ValueError
        # Check for a property with the value
        if self.has_attribute('objsub_' + code):
            return(str(self.get_attribute('objsub_' + code)))
        # Otherwise return None, which should cause the substitution to be ignored
        return(None)
