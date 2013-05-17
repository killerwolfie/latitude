from ev import Player

class LatitudePlayer(Player):
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(LatitudePlayer, self).basetype_setup()
        # Clear any locks set by the default base
        self.locks.replace('')
        # Add some administrative locks.  These are used to control access to sensitive privilidged operations.
        # The locks control whether a user can even attempt to perform an action on the object, so the same locks are defined for all objects even if they only apply to certain types of objects.
        self.locks.add(";".join([
            "friend_add:false()",              # Permits users to add this player as a friend automatically.
            "friend_request:true()",           # Permits users to request to add this player as a friend.
        ]))

    def at_post_login(self, sessid):
        # Call @ic.  This will cause it to connect to the most recently puppeted object, by default
        # The connect command can (and probably does) modify the value of the most recently puppeted object to change the behavior of this call
        self.execute_cmd("@ic/nousage", sessid=sessid)

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
