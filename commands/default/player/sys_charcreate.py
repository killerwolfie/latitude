from ev import default_cmds, create_object, settings

class CmdSysCharCreate(default_cmds.MuxPlayerCommand):
    """
    Create a character

    Usage:
      @charcreate <charname>

    Create a new character. You may use upper-case
    letters in the name - you will nevertheless]
    always be able to access your character using
    lower-case letters if you want.
    """

    key = '@charcreate'
    aliases = []
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        "create the new character"
        player = self.caller
        if not self.args:
            self.msg("Usage: @charcreate <charname>")
            return
        key = self.args
        # Verify that the account has a free character slot
        max_characters = player.max_characters()
        playable_characters = player.db.get_playable_characters()
        if not player.is_superuser and len(playable_characters) >= max_characters:
            self.msg("You may only create a maximum of %i characters." % max_characters)
            return
        # Verify that the character name is not already taken

        # create the character
        from src.objects.models import ObjectDB

        default_home = ObjectDB.objects.get_id(settings.CHARACTER_DEFAULT_HOME)
        typeclass = settings.BASE_CHARACTER_TYPECLASS
        permissions = settings.PERMISSION_PLAYER_DEFAULT

        new_character = create_object(typeclass, key=key, location=default_home,
                                             home=default_home, permissions=permissions)
        # only allow creator (and admins) to puppet this char
        new_character.locks.add("puppet:id(%i) or pid(%i) or perm(Janitors)" % (new_character.id, player.id))
        # Set this new character as owned by this player
        new_character.db.owner = player
        # Configure the character as a new character in the world
        new_character.db.desc = "This is a Player."
        # Inform the user that we're done.
        self.msg("Created new character %s. Use {w@ic %s{n to enter the game as this character." % (new_character.key, new_character.key))
