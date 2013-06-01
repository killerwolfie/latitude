from ev import Player, utils, search_object, search_player
import time

class LatitudePlayer(Player):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudePlayer, self).basetype_setup()
        # Clear any locks set by the default base
        self.locks.replace('')
        # Create friend system variables
        self.db.friends_list = set()
        self.db.friends_requests = set()
        # Empty stats
        self.set_attribute('stats_last_login_time', None)
        self.set_attribute('stats_last_logout_time', None)

    def at_post_login(self, sessid):
        # Call @ic.  This will cause it to connect to the most recently puppeted object, by default
        # The connect command can (and probably does) modify the value of the most recently puppeted object to change the behavior of this call
        self.execute_cmd("@ic/nousage", sessid=sessid)
        self.execute_cmd("@friends", sessid=sessid)
        if self.db.msg_unseen:
            self.msg('{GYou have unread messages.  Type "@page" to read them.  See "help @page" for more information.')
        # Update same statistics
        self.db.stats_last_login_time = time.time()
        if self.db.stats_times_login:
            self.db.stats_times_login += 1
        else:
            self.db.stats_times_login = 1

    def at_disconnect(self, reason=None):
        # Update some statistics
        self.db.stats_last_logout_time = time.time()

    def return_title(self, looker):
        """
        Returns the name of this player, styled (With colors, etc.) to help identify
        the type of the object.  This is used for compatibility with
        LatitudeObject.return_title() objects.  For more details, look there.
        """
        # You shouldn't create any Objects directly.  This is meant to be a pure base class.
        # So, make an accordingly ominous looking name.
        if self.status_online():
            return '{m' + self.key
        else:
            return '{M' + self.key

    def status_online(self):
        """
        Returns the amount of time a player has been online.

        It takes 'friend system' privacy into account, returning 'None' if only private characters are puppeted.
        """
        # If we're actually offline then we'll show that way.
        if not self.sessions:
            return None
        # If we have any un-hidden puppets, then we'll show as online
        puppets = self.get_all_puppets()
        if puppets:
            only_optout = True
            for char in puppets:
                if not char.db.friends_optout:
                    only_optout = False
                    break
        else:
            # If we have no puppets, then we'll show as online.
            only_optout = False
        if only_optout:
            return None
        # Looks like we're online and we want to show that way.  Return seconds online of the longest lived session.
        now = time.time()
        online_time = float('-inf')
        for session in self.sessions:
            session_online = now - session.conn_time
            if session_online > online_time:
                online_time = session_online
        return online_time

    def status_idle(self):
        """
        Returns the idle time of the player, in seconds.

        Returns None if the player is offline.
        """
        if self.status_online():
            now = time.time()
            idle_time = float('inf')
            # Return the session with the lowest idle time
            for session in self.sessions:
                session_idle = now - session.cmd_last_visible
                if session_idle < idle_time:
                    idle_time = session_idle
            return idle_time
        else:
            return None

    def max_characters(self):
        """
        Get the maximum number of characters this player is allowed to have associated with their account
        """
        # Admins can have as many characters as they want
        if 'Janitors' in self.permissions or 'Custodians' in self.permissions:
            return float('inf')
        # Start with the default number of characters
        max_characters = 5
        # Apply bonuses
        if self.db.account_manualbonus_characters:
            max_characters += self.db.account_manualbonus_characters
        return max_characters

    def get_playable_characters(self, online_only=False):
        """
        Return a list of playable characters associated with this player.
        Objects will be validly considered your character if:
            1) The object's 'owner' attribute matches your player
            2) The object is a valid character object
            3) The object's name does not match the name of any other character (case insensitive)
            4) The object's name does not match the name of any player, except yours (case insensitive)
        """
        if online_only:
            character_candidates = self.get_all_puppets()
        else:
            character_candidates = search_object(self.key, attribute_name='owner') # TODO: Try searching by typeclass here for speed
        characters = []
        for character in character_candidates:
            # Verify that we are the owner of this object
            if not character.db.owner.lower() == self.key.lower():
                continue
            # Verify that this is actually a character object
            if not utils.inherits_from(character, "src.objects.objects.Character"):
                continue
            # Verify that, among character objects, this one has a unique name
            if len([char for char in search_object(character.key, attribute_name='key') if utils.inherits_from(char, "src.objects.objects.Character")]) != 1:
                continue
            # Verify this doesn't match the name of any player, unless that player is self
            if character.key.lower() != self.key.lower():
                if search_player(character.key):
                    continue
            characters.append(character)
        return characters

    def is_friends_with(self, player):
        """
        Retuns whether a this player is friends with another player.  (Friendship is always mutual)
        """
        if not player or player == self:
            return False
        return self in player.db.friends_list and player in self.db.friends_list

    def get_friend_players(self, online_only=False):
        """
        Get a list of this player's friend players.  (Friendship is always mutual)
        """
        # If there are any deleted players in the friend list, clear them out
        if None in self.db.friends_list:
            self.db.friends_list.remove(None)
        # Although it's a touching sentiment, you can't add yourself to your friend list and expect it to work
        if self in self.db.friends_list:
            self.db.friends_list.remove(self)
        # Generate the list of friends
        friend_players = set()
        for friend in self.db.friends_list:
            if self.is_friends_with(friend):
                if not online_only or friend.status_online():
                    friend_players.add(friend)
        return friend_players

    def get_friend_characters(self, online_only=False):
        """
        Get a list of all the characters of this player's friends.
        Friendship between players is always mutual, but individual characters can be flagged as hidden from the friend system.
        """
        # Build up a set of characters and return
        friend_characters = set()
        for friend_player in self.get_friend_players():
            for friend_character in friend_player.get_playable_characters(online_only=online_only):
                if friend_character.db.friends_optout:
                    continue
                if online_only and not (friend_character.status_online() or friend_character.player):
                    continue
                friend_characters.add(friend_character)
        return friend_characters

    def get_friends_optout(self):
        """
        Returns whether any currently connected characters are opped out from the friend system.
        """
        for char in self.get_all_puppets():
            if char.db.friends_optout:
                return True
        return False
