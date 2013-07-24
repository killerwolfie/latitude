from game.gamesrc.latitude.objects.object import Object
from ev import utils, search_object

def _color_at_depth(depth_spec, depth):
    """
    Grab the highest attribute available which is at this depth or below.
    """
    # By default take the lowest depth, even if it's higher than the requested depth
    best_depth = min(depth_spec)
    for this_depth in depth_spec:
        if int(this_depth) <= int(depth) and int(this_depth) > int(best_depth):
            best_depth = this_depth
    return depth_spec[best_depth]

class Actor(Object):
    """
    Base class for defining objects which have will.
    They can bare equipment, perform actions, have stats, bare status conditions and bonuses, etc.
    This includes mobs and characters.
    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(Actor, self).basetype_setup()
        self.db.equipment = set()

    def bad(self):
        # Equipment
        for item in self.db.equipment:
            if item.get_equipper() != self:
                return 'character and item data conflict (%s)' % item.key

    def at_after_move(self, source_location):
        # Display the new location so the user gets an indication that they've moved
        if self.player:
            self.player.at_display_context(self.sessid)
        # Clear 'following', if needed.
        following = self.db.follow_following
        if following and (following.location == None or following.location != self.location):
            self.msg('You move off, and stop following %s.' % (following.key))
            following.msg('%s moves off, and stops following you.' % (self.key))
            del self.db.follow_following
        # Clear any pending follow or lead requests
        del self.db.follow_wantfollow
        del self.db.follow_wantlead

    def at_desc_scent(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg(self.objsub('&1N just smelled you!', looker))
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just smelled &0d.', looker), exclude=[self, looker])

    def at_desc_flavor(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg(self.objsub('&1N just tasted you!', looker))
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just tasted &0d.', looker), exclude=[self, looker])

    def at_desc_texture(self, looker):
        if not looker.location or (not looker.location == self.location and not looker.location == self):
            return()
        self.msg(self.objsub('&1N just felt you!', looker))
        if looker.location:
            looker.location.msg_contents(self.objsub('&1N just felt &0d.', looker), exclude=[self, looker])

    # ----- Descriptions -----
    def _desc_mod(self, method, value, additional_args={}):
        """
        Return a value which is modified by any active mods.
        """
        max_prio = (float('-inf'), float('-inf'))
        retval = value
        for mod in self.get_mods():
            this_prio = (mod.mod_priority(), mod.__hash__())
            if this_prio < max_prio:
                # We already have a higher priority than this
                continue
            new_desc = getattr(mod, method)(value, **additional_args)
            if new_desc == None:
                # Script doesn't provide a mod for this
                continue
            # New winner
            max_prio = this_prio
            retval = new_desc
        return retval

    def get_desc_styled_name(self, looker=None):
        # You shouldn't create any Actors directly.  This is meant to be a pure base class.
        # So, make an accordingly ominous looking name.
        return '{x<(' + self.key + ')>'

    def get_desc_appearance(self, looker=None):
        return self._desc_mod('mod_appearance', super(Actor, self).get_desc_appearance(looker=looker))

    def get_desc_contents(self, looker=None):
        """
        Returns the visual description of the object, if looking inside.
        """
        return self._desc_mod('mod_contents', super(Actor, self).get_desc_contents(looker=looker))

    def get_desc_scent(self, looker=None):
        return self._desc_mod('mod_scent', super(Actor, self).get_desc_scent(looker=looker))

    def get_desc_texture(self, looker=None):
        return self._desc_mod('mod_texture', super(Actor, self).get_desc_texture(looker=looker))

    def get_desc_flavor(self, looker=None):
        return self._desc_mod('mod_flavor', super(Actor, self).get_desc_flavor(looker=looker))

    def get_desc_sound(self, looker=None):
        return self._desc_mod('mod_sound', super(Actor, self).get_desc_sound(looker=looker))

    def get_desc_aura(self, looker=None):
        return self._desc_mod('mod_aura', super(Actor, self).get_desc_aura(looker=looker))

    def get_desc_writing(self, looker=None):
        return self._desc_mod('mod_writing', super(Actor, self).get_desc_writing(looker=looker))

    def get_desc_gender(self, looker=None):
        return self._desc_mod('mod_gender', super(Actor, self).get_desc_gender(looker=looker))

    def get_desc_species(self, looker=None):
        return self._desc_mod('mod_species', super(Actor, self).get_desc_species(looker=looker))

    # ----- Maps -----
    def get_desc_map(self, mark_friends_of=None):
        """
	Return an ascii image representing the location of the object for helping users to navigate.
	"""
	room = self.get_room()
	if hasattr(room, 'get_desc_map'):
	    return room.get_desc_map(mark_friends_of)
	return None

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
        depth_spec = self.speech_color_depth()
        last_change = 1
	msg_sections = []
        for msg_section in msg_string.replace('%', '%%').replace('{', '{{').split('"'):
            msg_sections.append(_color_at_depth(depth_spec, current_color >= min_depth and current_color or min_depth) + msg_section)
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
        return self._desc_mod('mod_speech_name', self.db.say_name or self.key)

    def speech_says(self):
        """
        Returns this object's 'says' verb, used for constructing speech messages.
        """
        return self._desc_mod('mod_speech_says', self.db.say_says or "says")

    def speech_asks(self):
        """
        Returns this object's 'asks' verb, used for constructing speech messages.
        """
        return self._desc_mod('mod_speech_asks', self.db.say_asks or "asks")

    def speech_exclaims(self):
        """
        Returns this object's 'exclaims' verb, used for constructing speech messages.
        """
        return self._desc_mod('mod_speech_exclaims', self.db.say_exclaims or "exclaims")

    def speech_color_name(self):
	return self._desc_mod('mod_speech_color_name', self.db.say_color_name or '%ch%cc')

    def speech_color_quote(self):
	return self._desc_mod('mod_speech_color_quote', self.db.say_color_quote or '%cn%cw')

    def speech_color_depth(self):
        retval = {}
        for attr in self.get_all_attributes():
            if not attr.key.startswith('say_color_depth'):
                continue
            this_depth = attr.key[15:]
            if not this_depth.isdigit():
                continue
            retval[int(this_depth)] = attr.value
        if not retval:
            retval = {0: '{C', 1: '{W'}
	return self._desc_mod('mod_speech_color_depth', self.db.say_color_depth or retval)

    # ---- 'Attributes' ----
    def game_attribute(self, attribute, base=None):
        """
        Returns a character/npc/etc 'attribute', or 'stat' value.  (Not to be confused
        with the class's attributes or database attributes)  These are integers which
        represent the abilities of the object.
        """
        if base == None:
            base = 0
        value = int(base)
        mods = self.get_mods()
        # Check for any 'set' modifiers.  These override everything
        setter_value = None
        setter_priority = None
        for mod in mods:
            values = mod.mod_attr_set()
            if not values or not attribute in values:
                continue
            value = int(values[attribute])
            priority = (mod.priority(), mod.__hash__()) # The hash is included so that there's never a tie
            if setter_value == None or setter_priority < priority:
                setter_value = value
                setter_priority = priority
        if setter_value:
            return setter_value
        # Stacking offset
        for mod in mods:
            offset = mod.mod_attr_offset_stack()
            if not offset or not attribute in offset:
                continue
            offset = int(offset[attribute])
            if offset:
                value += offset
        # Non-stacking offset
        positive_non_stacking_offset = 0
        negative_non_stacking_offset = 0
        for mod in mods:
            offset = mod.mod_attr_offset_nostack()
            if not offset or not attribute in offset:
                continue
            offset = int(offset[attribute])
            # Non stacking offsets are applied at the end, once we figure out the best one(s)
            if offset > 0:
                if offset > positive_non_stacking_offset:
                    positive_non_stacking_offset = offset
            else:
                if offset < negative_non_stacking_offset:
                    negative_non_stacking_offset = offset
        value += positive_non_stacking_offset
        value += negative_non_stacking_offset
        # Stacking multiplier
        for mod in mods:
            multiplier = mod.mod_attr_multiply_stack()
            if not multiplier or not attribute in multiplier:
                continue
            multiplier = float(multiplier[attribute])
            if multiplier:
                value *= multiplier
        # Non stacking multiplier
        positive_non_stacking_multiplier = 1
        negative_non_stacking_multiplier = 1
        for mod in mods:
            multiplier = mod.mod_attr_multiply_nostack()
            if not multiplier or not attribute in multiplier:
                continue
            multiplier = float(multiplier[attribute])
            # Non stacking multipliers are applied at the end, once we figure out the best one(s)
            if multiplier > 1:
                if multiplier > positive_non_stacking_multiplier:
                    positive_non_stacking_multiplier = multiplier
            else:
                if multiplier < negative_non_stacking_multiplier:
                    negative_non_stacking_multiplier = multiplier
        value *= positive_non_stacking_multiplier
        value *= negative_non_stacking_multiplier
        return int(value)

    def game_attribute_current(self, attribute):
        """
        Returns the current value of an attribute, taking stat offsets into account.

        Attributes are normally fixed, and can only be changed by modifying the
        object's equipment, scripts, etc.  But some attributes need to change all the
        time and are largely temporary.  So this routine checks and accounts for
        attr_offset_<stat> properties on the object.

        For example, game_attribute() for maximum magic, and game_attribute_current()
        for current magic, and modify obj.db.attr_offset_magic to consume (or boost
        past max) your magic.  Gradual recovery can be done with a script by finding
        objects with an offset, and moving it toward 0.

        This can also be used in the same way for counter-like attributes, which have
        no maximum, such as gold or experience points.

        Bare in mind that stat multiplier mods affect the values returned by
        game_attribute(), and are not affected by the offset value of the attribute.

        The offsets may be fractional, but only whole numbers (rounded down) are
        returned.
        """
        offset = self.get_attribute('attr_offset_' + attribute) or 0
        return int(self.game_attribute(attribute) + offset)

    def game_attribute_offset(self, attribute, offset, keep_small_values=False):
        """
        Apply an offset to an attribute on this object, and msg the object about it.
        Returns the output of game_attribute_offset_message()

        If the resulting offset is between -0.5 and 0.5, then it will be rounded to 0
        and cleared, unless keep_small_values is specified, in which case it will only
        be cleared if it equals 0.
        """
        if int(offset):
            curval = self.get_attribute('attr_offset_' + attribute) or 0
            newval = curval + int(offset)
            if newval == 0 or (not keep_small_values and newval > -0.5 and newval < 0.5):
                self.del_attribute('attr_offset_' + attribute)
            else:
                self.set_attribute('attr_offset_' + attribute, newval)
        return self.game_attribute_offset_message(attribute, offset)

    def game_attribute_offset_message(self, attribute, offset):
        """
        Produces a short message to describe a game attribute offset.
        Examples:
            (-5 magic)
            (10XP)
            (earned 10 gold)
            (2 damage!)
        """
        # Generate and return message
        if offset < 0:
            message = '{Y(%d %s)' % (offset, attribute)
        elif offset > 0:
            message = '{G(+%d %s)' % (offset, attribute)
        else:
            message = '{Y(%s unchanged)' % (attribute)
        return message

    # ---- Equipment / Status Effects / Etc. ----
    def get_equipment(self, slot=None):
        """
        Return a list of equipment equipped by this Object.
        """
        if slot:
            return set(item for item in self.db.equipment if item and item.get_equipper() == self and item.equipment_slot() == slot)
        else:
            return set(item for item in self.db.equipment if item and item.get_equipper() == self)

    def get_mods(self, slot=None):
        """
        Returns a set of Mod objects which apply to this Object.
        """
        self.scripts.validate()
        # Produce a list of all objects, which if derived from Mod, qualify on this character
        candidates = set(self.get_equipment())
        for script in self.scripts.all():
            candidates.add(script)
        candidates.add(self.location)
        # TODO: Global mods
        # Return the set of mods
        return set(candidate for candidate in candidates if utils.inherits_from(candidate, 'game.gamesrc.latitude.struct.mod.Mod'))

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

    # ----- Object based string substitution -----

    # I - Indefinite Name
    def objsub_b(self):
        return 'someone'

    # D - Definite Name
    def objsub_c(self):
        return 'the ' + self.get_desc_species().lower()

    # D - Definite Name
    def objsub_d(self):
        return self.key

    # I - Indefinite Name
    def objsub_i(self):
        return self.key
