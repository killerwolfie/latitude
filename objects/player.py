"""

Template module for Players

Copy this module up one level and name it as you like, then
use it as a template to create your own Player class.

To make the default account login default to using a Player
of your new type, change settings.BASE_PLAYER_TYPECLASS to point to
your new class, e.g.

settings.BASE_PLAYER_TYPECLASS = "game.gamesrc.objects.myplayer.MyPlayer"

Note that objects already created in the database will not notice
this change, you have to convert them manually e.g. with the
@typeclass command.

"""
from ev import Player

class LatitudePlayer(Player):
    """
    This class describes the actual OOC player (i.e. the user connecting
    to the MUD). It does NOT have visual appearance in the game world (that
    is handled by the character which is connected to this). Comm channels
    are attended/joined using this object.

    It can be useful e.g. for storing configuration options for your game, but
    should generally not hold any character-related info (that's best handled
    on the character level).

    Can be set using BASE_PLAYER_TYPECLASS.


    * available properties

     key (string) - name of player
     name (string)- wrapper for user.username
     aliases (list of strings) - aliases to the object. Will be saved to database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
     dbobj (Player, read-only) - link to database model. dbobj.typeclass points back to this class
     typeclass (Player, read-only) - this links back to this class as an identified only. Use self.swap_typeclass() to switch.
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     user (User, read-only) - django User authorization object
     obj (Object) - game object controlled by player. 'character' can also be used.
     sessions (list of Sessions) - sessions connected to this player
     is_superuser (bool, read-only) - if the connected user is a superuser

    * Handlers

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().

    * Helper methods

     msg(outgoing_string, from_obj=None, data=None)
     swap_character(new_character, delete_old_character=False)
     execute_cmd(raw_string)
     search(ostring, global_search=False, attribute_name=None, use_nicks=False, location=None, ignore_errors=False, player=False)
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hook methods (when re-implementation, remember methods need to have self as first arg)

     basetype_setup()
     at_player_creation()

     - note that the following hooks are also found on Objects and are
       usually handled on the character level:

     at_init()
     at_cmdset_get()
     at_first_login()
     at_post_login()
     at_disconnect()
     at_message_receive()
     at_message_send()
     at_server_reload()
     at_server_shutdown()

    """
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
            "admin_alias:pperm(Janitors)",     # Permits the use of administrative commands to modify the object's aliases
            "admin_examine:pperm(Janitors)",   # Permits the use of administrative commands to examine the object and its properties
            "admin_delete:pperm(Janitors)",    # Permits the use of administrative commands to delete the object
            "admin_set:pperm(Janitors)",       # Permits the use of administrative commands to set properties on the object
            "admin_rename:pperm(Janitors)",    # Permits the use of administrative commands to rename the object
            "admin_typeclass:pperm(Janitors)", # Permits the use of administrative commands to change the typeclass of this object
            "admin_perm:pperm(Janitors)",      # Permits the use of administrative commands to set 'permissions' on this object  (Also can't give permissions that exceed the permissions of the user)
            "admin_script:pperm(Janitors)",    # Permits the use of administrative commands to attach scripts to this object
            "admin_boot:pperm(Janitors)",      # Permits the use of administrative commands to boot the user
            "admin_ban:pperm(Janitors)",       # Permits the use of administrative commands to ban the user
            "friend_add:false()",              # Permits users to add this player as a friend automatically.
            "friend_request:true()",           # Permits users to request to add this player as a friend.
        ]))
        self.locks.add("msg:all()")

    def at_post_login(self, sessid):
        if not self.character:
	    # We logged in OOCly
	    self.execute_cmd('look', sessid=sessid)
