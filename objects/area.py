from ev import utils
from game.gamesrc.latitude.objects.object import Object
from game.gamesrc.latitude.commands.area.cmdset import AreaCmdSet
from random import choice

class Area(Object):
    """
    This object is a container for rooms, and it handles various functions relating to a localized vacinity in the game world, such as map data.
    """

    def at_object_creation(self):
        super(Area, self).at_object_creation()
        self.locks.add('call:true()')
        self.locks.add('leave:true()')
        self.cmdset.add(AreaCmdSet, permanent=True)
        self.db.area_visit_landmark = False
        self.db.area_visit_residence = True
        self.db.area_visit_map = True
        self.db.area_visit_friends = True
        self.db.area_visit_self = True

    def bad(self):
        if not self.location or not utils.inherits_from(self.location, 'game.gamesrc.latitude.objects.region.Region'):
            return 'area has no region'
        area_spawn = self.db.area_spawn
        if area_spawn:
            for spawn_point in area_spawn:
                if not spawn_point in self.contents:
                    return 'area has spawn point outside area'
                if not utils.inherits_from(spawn_point, 'src.objects.objects.Room'):
                    return 'area spawn point is not a room'
        return super(Area, self).bad()

    def get_desc_styled_name(self, looker=None):
        return '{M[' + self.key + ']'

    def get_desc_appearance(self, looker=None):
        return '{w%s\n{x[Use "leave" to return to the region menu]' % (self.key)

    def get_desc_contents(self, looker=None):
        return self.get_desc_appearance(looker=looker)

    def can_visit(self, character):
        """
        Returns whether a given character can explicitly visit this area (Without 'wandering').
        - If not, then None or [] is returned.
        - If so, then a list of short strings is returned explaining why. ('Landmark' for everyone has access.  'Known' for character just knows the way there.)

        By default None is returned, unless one or more of the following are true:
            - If self.db.area_visit_landmark is true.
            - self.db.area_visit_friends is true, and a friend of this character is located in the area.
            - self.db.area_visit_self is true, and one of your other characters is located in this area
            - self.db.area_visit_map is true, and the character has a item that references this area. (item_obj.db.area_maps_to)
            - self.db.area_visit_residence is true, and the character is a resident of a room in the area.

        Eg.
            'Landmark'
            'Residence'
            'Night Vision'
            'A tattered treasure map'
            'Billy'
            'From a dream', 'Billy', 'Residence'
        """
        player = character.player
        ok_reasons = []
        # Landmarks
        if self.db.area_visit_landmark:
            ok_reasons.append('Landmark')
        # Friends
        if self.db.area_visit_friends:
            for friend_character in player.get_friend_characters(online_only=True):
                if friend_character.get_area() == self:
                    ok_reasons.append(friend_character.get_desc_styled_name())
        # Residents
        if self.db.area_visit_residence:
            for area_room in self.contents:
                if area_room.db.resident == character:
                    ok_reasons.append('{wResident')
                    break
        # Maps
        if self.db.area_visit_map:
            for item in character.contents:
                if item.db.area_maps_to == self:
                    ok_reasons.append(item.get_desc_styled_name())
        # Self
        if self.db.area_visit_self:
            for self_character in player.get_all_puppets():
                if not self_character == character and self_character.get_area() == self:
                    ok_reasons.append(self_character.get_desc_styled_name())
        # Return result
        return ok_reasons

    def can_wander_to(self, character):
        """
        Returns whether a given character can wander to this area.

        By default, all areas can be wandered to unless they're an instance.  (The wander routine should never consider instance areas anyway)
        """
        return not self.db.area_instance

    def move_redirect(self, obj):
        """
        Redirect for redirectable_move_to requests.
        By default, areas redirect users to one of its spawn points at random.
        """
        if utils.inherits_from(obj, 'game.gamesrc.latitude.objects.character.Character'):
            spawn = self.db.area_spawn
            if spawn:
                return choice(list(spawn))
        return None
