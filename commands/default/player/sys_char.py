from game.gamesrc.latitude.utils.evennia_color import *
from game.gamesrc.latitude.utils.search import match_character
from ev import settings, utils, search_object, search_player, create_object
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysChar(LatitudeCommand):
    """
    @char - Manage your characters

    Usage:
      look (Only when OOC)
        Displays a welcome message, along with your character listing, and
        instructions on how to go IC and play.

      @char
      @char/list
          Display a list of all your available characters.

      @ic
      @ic <character name>
      @char/ic <character name>
        Use this to 'become' a character.  Your current session (but none of your
        other sessions, if you happen to be connected multiple times) will assume
        the identity of the selected character, and you'll be able to percieve the
        game world and play.

        If you don't supply a character name, it attempt to will pick one for you
        automatically (Such as the last character you used)

      @ooc
      @char/ooc
          Disconnects yourself from your character, and returns you to the connection
          screen, as though you've just logged in
      
      @char/new <character name>
          Creates a new character.

      @char/del <character name>=<password>
          Murder one of your helpless characters.  :(  You need to enter your password
          to preent accidental deletion.  You monster.

          {rWARNING:{n Deleting a character will not release that character's name.  If
          you want to recreate your character, you'll have to select a new name.
    """

    key = "@char"
    aliases = ['@ic', '@ooc']
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        args = self.args
        switches = [switch.lower() for switch in self.switches]

        if self.cmdstring.lower() == '@ic' and not switches:
            self.cmd_ic()
            return
        elif self.cmdstring.lower() == '@ooc' and not switches and not args:
            self.cmd_ooc()
            return
        else:
            if (switches == [ 'list' ] or not switches) and not self.args:
                self.cmd_list()
                return
            elif self.switches == [ 'ic' ]:
                self.cmd_ic()
                return
            elif self.switches == [ 'ooc' ] and not self.args:
                self.cmd_ooc()
                return
            elif self.switches == [ 'new' ] and self.args:
                self.cmd_new()
                return
            elif self.switches == [ 'del' ] and self.lhs:
                self.cmd_del()
                return
        # Unrecognized command
        self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))

    def cmd_list(self):
        player = self.player
        characters = sorted(player.get_characters(), cmp=lambda a, b: cmp(a.key,b.key))
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")
        self.msg('{CYour characters:')
        for char in characters:
            self.msg('  ' + char.get_desc_styled_name(player))
        if player.no_slot_chars():
            self.msg('\n{RYou appear to have more characters than character slots.  Some of your characters may be inaccessible.')
            self.msg('{RIf you believe this is an error, please contact {rstaff@latitude.muck.ca{R.')
        self.msg("{x________________{W_______________{w_______________{W_______________{x_________________")

    def cmd_new(self):
        player = self.player
        key = self.args
        # Verify that the account has a free character slot
        max_characters = player.max_characters()
        playable_characters = player.get_characters()
        if len(playable_characters) >= player.max_characters():
            self.msg("{RYou may only create a maximum of %i characters." % max_characters)
            return
        # Check the character name
        if re.search('[^a-zA-Z0-9._-]', key) or not (3 <= len(key) <= 20):
            self.msg('{R[Character names must be between 3 and 20 characters, and only contain english letters, numbers, dot (.), underscore (_), or dash(-)]')
            return
        # Verify that the character name is not already taken
        for existing_object in search_object(key, attribute_name='key'):
            if utils.inherits_from(existing_object, "src.objects.objects.Character"):
                self.msg("{R[That character name is already taken]")
                return
        # Verify that this is not the name of a player, unless it's your own
        if key.lower() != player.key.lower():
            if search_player(key):
                self.msg("{R[That name is already taken by a player account]")
                return
        # create the character
        from src.objects.models import ObjectDB
        default_home = ObjectDB.objects.get_id(settings.CHARACTER_DEFAULT_HOME)
        typeclass = settings.BASE_CHARACTER_TYPECLASS
        permissions = settings.PERMISSION_PLAYER_DEFAULT
        new_character = create_object(typeclass, key=key, location=default_home, home=default_home, permissions=permissions)
        # only allow creator (and admins) to puppet this char
        new_character.locks.add("puppet:id(%i) or pid(%i) or perm(Janitors)" % (new_character.id, player.id))
        # Set this new character as owned by this player
        new_character.set_owner(player)
        # Configure the character as a new character in the world
        new_character.db.desc = "This is a Player."
        # Inform the user that we're done.
        self.msg("{G[Created new character %s. Use {g%s/ic %s{G to enter the game as this character]" % (new_character.key, self.key, new_character.key))

    def cmd_ic(self):
        player = self.player
        characters = player.get_characters()
        # Determine which character to occupy
        if self.args:
            target = match_character(self.args)
            if not target or not target in characters:
                self.msg("{R[That's not a valid character selection]")
                return
        else:
            target = player.last_puppet()
            if not target or not target in characters:
                self.msg("{R[Please specify a character.  See {r%s/list{R for a list]" % (self.key))
                return
        # Puppet the character (and output success/failure messages)
        player.do_puppet(self.sessid, target)
        player.at_display_context(self.sessid)

    def cmd_ooc(self):
        # Unpuppet the character (and output success/failure messages)
        self.player.do_unpuppet(self.sessid)

    def cmd_del(self):
        player = self.player
        characters = player.get_characters()
        # Find the character to nuke
        target = match_character(self.lhs)
        if not target:
            self.msg("{R[That's not a valid character selection]")
            return
        # Ensure you have permissions
        if not player.check_password(self.rhs):
            self.msg("{R[Password incorrect]")
            return
        if not target.access(player, 'char_delete'):
            self.msg("{R[You're not allowed to delete that character]")
            if target in characters:
                self.msg('{R[If you believe this is an error, please contact {rstaff@latitude.muck.ca{R]')
            return
        # Bye bye character
        target_player = target.player
        target_sessid = target.sessid
        # Bye bye character step 1: Unpuppet any player that's currently puppeted
        if target_player:
            target_player.do_unpuppet(target_sessid)
        # Bye bye character step 2: Send the character into the abyss and alert nearby objects
        if target.location:
            target.location.msg_contents('%s disappears.' % (target.key), exclude=[target])
        target.location = None
        target.set_owner(None)
        # Bye bye character step 3: Finalize the deletion, and alert the player(s) involved.
        target_name = target.key
        #target.delete()
        alertus = {player}
        if target_player:
            alertus.add(target_player)
        for alertme in alertus:
            alertme.msg('{R[The character "%s" has been deleted by {c%s{r]' % (target_name, player.get_desc_styled_name(alertme)))
