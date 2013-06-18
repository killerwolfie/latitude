from ev import Object as EvenniaObject
from ev import Exit as EvenniaExit
from ev import Room as EvenniaRoom
import re

class Object(EvenniaObject):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(Object, self).basetype_setup()
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
        if not isinstance(accessing_obj, Object):
            # Don't bother with players, or any other type of object which may be making an access call.
            # For one, we can't get a player's session id to send messages out.
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
            accessing_obj.msg('{R[ %s{R ]' % message, sessid=accessing_obj.sessid)

    def at_access_success(self, accessing_obj, access_type):
        # Check for a message property (sending nothing by default)
        if self.db.access_failure and access_type in self.db.access_failure and self.db.access_failure[access_type] != None:
            accessing_obj.msg(self.db.access_failure[access_type])

    # ----- Auditing -----
    def bad(self):
        """
        Audits whether the object is corrupted in some way, such as being a direct
        instance of the Object class, rather than a child class.

        If the character is valid, then None is returned.  If it's broken, then a
        string is returned containing a reason why.
        """
        if type(self) is Object:
            return "object is a base 'Object' class"
        return None

    # ----- Descriptions -----
    def return_styled_name(self, looker=None):
        """
        Returns the name of this object, styled (With colors, etc.) to help identify
        the type of the object.  This is used when displaying lists of objects, or
        examining the object data, or any other situation where it would be convenient
        to be able to identify the type of an object at a glance. (@who, @examine,
        inventory, the contents of rooms when doing a 'look', etc.)

        * This can also be used to create special glasses for administrators, where
        when you see the title of an object, it's accompanied by its database ID, or
        other technical details.

        * This can also be used to see at a glance whether a user is online or not.
        """
        # You shouldn't create any Objects directly.  This is meant to be a pure base class.
        # So, make an accordingly ominous looking name.
        return '{x<<' + self.key + '>>'

    def return_styled_gender(self, looker=None):
        """
        Returns the gender of this object, styled (With colors, etc.).
        """
        gender = self.return_gender()
        if not gender:
            gender = '%cn%cr-Unset-'
        elif self.is_male():
            gender = '%cn%ch%cb' + gender
        elif self.is_female():
            gender = '%cn%ch%cm' + gender
        elif self.is_herm():
            gender = '%cn%ch%cg' + gender
        else:
            gender = '%cn%ch%cw' + gender
        return gender

    def return_appearance(self, looker=None):
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

    def return_appearance_name(self, looker=None):
        """
	Return the name portion of the visual description.
	By default, the name of the object is not announced when getting the description.
	"""
        return(None)

    def return_appearance_desc(self, looker=None):
        """
	Return the main portion of the visual description.
	"""
        desc = self.db.desc_appearance
	if desc != None:
	    return('%cn' + desc)
	else:
	    return('%cnYou see nothing special.')

    def return_appearance_exits(self, looker=None):
        """
	Return a line that describes the visible exits in the object.
	"""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker)
        exits = []
        for con in visible:
            if isinstance(con, EvenniaExit):
                exits.append(con.key)

        if exits:
            return('%ch%cx[Exits: ' + ', '.join(exits) + ']%cn')
	else:
	    return(None)

    def return_appearance_contents(self, looker):
        """
	Return a descriptive list of the contents held by this object.
	"""
        visible = [con for con in self.contents if con != looker]
        exits, users, things = [], [], []
        for con in visible:
            if isinstance(con, EvenniaExit):
	        exits.append(con.key)
            elif con.player:
                users.append(con.return_styled_name(looker))
            else:
                things.append(con.return_styled_name(looker))
        if users or things:
            string = self.return_appearance_contents_header(looker)
            if users:
                string += '\n%ch%cc' + '\n'.join(users) + '%cn'
            if things:
                string += '\n%cn%cc' + '\n'.join(things) + '%cn'
            return(string)
	else:
	    return(None)

    def return_appearance_contents_header(self, looker=None):
        """
	Returns a header line to display just before outputting the contents of the object.
	"""
        return('%ch%cbContents:%cn')

    def return_scent(self, looker=None):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_scent:
	    return self.db.desc_scent
	else:
	    return self.objsub("&0C doesn't seem to have any descernable scent.")

    def return_texture(self, looker=None):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_texture:
	    return self.db.desc_texture
	else:
	    return self.objsub("&0C doesn't seem to have any descernable texture.")

    def return_flavor(self, looker=None):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_flavor:
	    return self.db.desc_flavor
	else:
	    return self.objsub("&0C doesn't seem to have any descernable flavor.")

    def return_sound(self, looker=None):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_sound:
	    return self.db.desc_sound
	else:
	    return self.objsub("&0C doesn't seem to have any descernable sound.")

    def return_aura(self, looker=None):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_aura:
	    return self.db.desc_aura
	else:
	    return self.objsub("&0C doesn't seem to have any descernable aura.")

    def return_writing(self, looker=None):
        """
	Returns the scent description of the object.
	"""
        if self.db.desc_writing:
	    return self.db.desc_writing
	else:
	    return self.objsub("&0C doesn't seem to have any descernable writing.")

    def return_gender(self, looker=None):
        """
        Returns the gender description of the object.  (Typically one word)
        """
        if self.db.desc_gender:
            return self.db.desc_gender
        else:
            return 'thing'

    def return_species(self, looker=None):
        """
        Returns the species description of the object.  (Typically less than 25 characters)
        """
        if self.db.desc_species:
            return self.db.desc_species
        else:
            return 'Object'

    # ----- Speech -----
    def speech_say(self, say_string, pose=False):
        """
        Take a string of words this object wants to say, and return a stylized string, suitable for messaging to others.
        """
        # Determine verb
        if say_string.endswith('?'):
	    verb = self.speech_asks()
	elif say_string.endswith('!'):
	    verb = self.speech_exclaims()
	else:
	    verb = self.speech_says()
	return self.speech_color_name() + self.speech_name() + ' ' + self.speech_msg(verb + ', "' + say_string + '"')

    def speech_pose(self, pose_string):
        """
        Take a string of words this object wants to 'pose', and return a stylized string, suitable for messaging to others.
        """
        sep = ' '
        if [chk for chk in ["'s ", '-', ', ', ': ', ' '] if pose_string.startswith(chk)]:
            sep = ''
        return(self.speech_color_name() + self.speech_name() + sep + self.speech_msg(pose_string))

    def speech_msg(self, msg_string, min_depth=0):
        """
        Process a message which this object wants to say, pose, whisper, etc. and stylize it with this object's speech style.

        Typically this just adds some color, but it could be used to modify the object's words as well (Such as adding exclamatory suffixes, cleaning up swears, etc.)
        """
        retval = u''
        current_color = min_depth
        last_change = 1
	msg_sections = []
        for msg_section in msg_string.replace('%', '%%').replace('{', '{{').split('"'):
            msg_sections.append(self.speech_color_depth(current_color >= min_depth and current_color or min_depth) + msg_section)
	    if msg_section == '':
	        current_color += last_change
	    elif msg_section[-1] == ' ':
	        current_color += 1
		last_change = 1
            else:
	        current_color -= 1
		last_change = -1
        return((self.speech_color_quote() + '"').join(msg_sections))

    def speech_name(self):
        """
        Returns this object's name, used for constructing speech messages.
        """
        return self.db.say_name or self.key

    def speech_says(self):
        """
        Returns this object's 'says' verb, used for constructing speech messages.
        """
        return self.db.say_says or "says"

    def speech_asks(self):
        """
        Returns this object's 'asks' verb, used for constructing speech messages.
        """
        return self.db.say_asks or "asks"

    def speech_exclaims(self):
        """
        Returns this object's 'exclaims' verb, used for constructing speech messages.
        """
        return self.db.say_exclaims or "exclaims"

    def speech_color_name(self):
	return self.db.say_color_name or '%ch%cc'

    def speech_color_quote(self):
	return self.db.say_color_quote or '%cn%cw'

    def speech_color_depth(self, depth):
        if depth > 10:
            depth = 10 # Depth limit, to limit recursion
        if self.get_attribute('say_color_depth' + str(depth)):
	    return self.get_attribute('say_color_depth' + str(depth))
        if depth < 1:
	    return '{C'
        elif depth == 1:
            return '{W'
        else:
            return self.speech_color_depth(depth - 1)

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
        return self.return_gender().lower().strip() in ['male', 'man', 'boy', 'dude', 'him']

    def is_female(self):
        return self.return_gender().lower().strip() in ['female', 'woman', 'girl', 'chick', 'lady', 'her']

    def is_herm(self):
        return self.return_gender().lower().strip() in ['herm', 'hermy', 'both', 'shemale']

    def is_neuter(self):
        return self.return_gender().lower().strip() in ['neuter', 'asexual', 'it', 'thing', 'object', 'machine', 'genderless', 'sexless']

    def is_androgynous(self):
        return not self.is_male() and not self.is_female() and not self.is_herm() and not self.is_neuter()

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

    def action_equip(self, equipper):
        """
        This action is called when a player attempts to 'equip' the object
        """
        equipper.msg("You can't put that on.")

    def action_unequip(self, unequipper):
        """
        This action is called when a player attempts to 'doff' the object
        """
        unequipper.msg("That's not something you can take off.")

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
            if isinstance(room.typeclass, EvenniaRoom):
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
    def at_after_move(self, source_location):
        super(Object, self).at_after_move(source_location)
        # Clear 'following'
        following = self.db.follow_following
        if following and (following.location == None or following.location != self.location):
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
            # Check for an attribute override first
            if self.has_attribute('objsub_' + code):
                return(str(self.get_attribute('objsub_' + code)))
            # Otherwise, use a function on the class
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
	if self.is_male():
	    return('his')
	if self.is_female():
	    return('hers')
        if self.is_herm():
	    return('hirs')
	if self.is_neuter():
	    return('its')
	return(self.key + "'s")

    # B - Casual Indefinite Name
    def objsub_b(self):
        """
        The casual name is used to order to casually or vaguely refer to the object, but expressed in an indefinite way (That is, not specific or unknown to the listener, such as with the idefinite article 'a')

        Examples:
            lamp post -> a lamp post
            Greywind Scaletooth -> an adventurer
            The Land Before Time -> a book
            a few pebbles -> pebbles
            [E]astern Gate -> a gate
            [E]xit Cave -> an exit
            The Courtyard -> a room

        In almost all cases, a character's name should be their casual name, but for objects it's often not.
        """
        return self.key

    # C - Casual Definite Name
    def objsub_c(self):
        """
        The casual name is used to order to casually or vaguely refer to the object, but expressed in a definite way (That is, specific or known to the listener, such as with the definite article 'the')

        Examples:
            lamp post -> the lamp post
            Greywind Scaletooth -> the adventurer
            The Land Before Time -> the book
            a few pebbles -> the pebbles
            [E]astern Gate -> the gate
            [E]xit Cave -> the exit
            The Courtyard -> the room

        In almost all cases, a character's name should be their casual name, but for objects it's often not.
        """
        return self.key

    # D - Specific Definite Name
    def objsub_d(self):
        """
        The name of the object when the object is specific or known to the listener.
        In other words, the name used in situations which typically call for the
        definite article.  ('the')

        Examples:
            lamp post -> the lamp post
            Greywind Scaletooth -> Greywind Scaletooth
            The Land Before Time -> The Land Before Time
            a few pebbles -> the pebbles
            [E]astern Gate -> the eastern gate
            [E]xit Cave -> the cave exit
            The Courtyard -> the courtyard
        """
        return 'the ' + self.key

    # I - Specific Indefinite Name
    def objsub_i(self):
        """
        The indefinite, (non-particular or unknown to the listenr) name of the object.
        In other words, the name used in situations which typically call for the
        indefinite article.  ('a')

        Examples:
            lamp post -> a lamp post
            Greywind Scaletooth -> Greywind Scaletooth
            The Land Before Time -> a copy of The Land Before Time
            a few pebbles -> a few pebbles
            [E]astern Gate -> an eastern gate
            [E]xit Cave -> a cave exit
            The Courtyard -> a courtyard

        Also, this doesn't mean 'vague'.  For example, you wouldn't want to change
        'King George' into 'a king'.  The user should still be able to identify what
        you're talking about, even though you're referring to it in an indefinite
        manner.  Although, for totally unique objects like 'King George' or 'The Holy
        Grail' there is no indefinite way to refer to them, in that case, just return
        their definite name.  (For 'vague', see 'B' - 'Casual Indefinite Name')
        """
        return 'a ' + self.key

    # N - Object Name
    def objsub_n(self):
        """
        This is the proper name of the object.
        Even though it's possible to override this, it would probably be bad, because it's used to identify the object to other players.
        It would allow a character to masquerade as another character, for example.  Not good.
        """
        return self.key

    # O - Objective Pronoun
    def objsub_o(self):
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
        return 'in ' + self.key

    # Other
    def objsub_other(self, code):
        return None
