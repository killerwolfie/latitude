"""
Commands that are available from the connect screen.
"""
import re
import traceback
from django.conf import settings
from django.contrib.auth.models import User
from src.players.models import PlayerDB
from src.objects.models import ObjectDB
from src.comms.models import Channel

from src.utils import create, logger, utils
from src.commands.default.muxcommand import MuxCommand

from ev import search_object

class CmdUnconnectedCreate(MuxCommand):
    """
    Create a new account.

    Usage (at login screen):
      create <playername> <password>
      create "player name" "pass word"

    This creates a new player account.

    If you have spaces in your name, enclose it in quotes.
    """
    key = "create"
    aliases = ["cre", "cr"]
    locks = "cmd:all()"

    def func(self):
        "Do checks and create account"

        session = self.caller
        args = self.args.strip()

        # extract quoted parts
        parts = [part.strip() for part in re.split(r"\"|\'", args) if part.strip()]
        if len(parts) == 1:
            # this was (hopefully) due to no quotes being found
            parts = parts[0].split(None, 1)
        if len(parts) != 2:
            string = "\n Usage (without <>): create <name> <password>"
            string += "\nIf <name> or <password> contains spaces, enclose it in quotes."
            session.msg(string)
            return
        playername, password = parts

        # Drop the player name to lowercase
        playername = playername.lower()
        # sanity checks
        if not re.findall('^[\w. @+-]+$', playername) or not (0 < len(playername) <= 30):
            # this echoes the restrictions made by django's auth module (except not
            # allowing spaces, for convenience of logging in).
            string = "\n\r Playername can max be 30 characters or fewer. Letters, spaces, digits and @/./+/-/_ only."
            session.msg(string)
            return
        # strip excessive spaces in playername
        playername = re.sub(r"\s+", " ", playername).strip()
        # Verify this player doesn't already exist
        if PlayerDB.objects.filter(user__username__iexact=playername) or User.objects.filter(username__iexact=playername):
            # player already exists (we also ignore capitalization here)
            session.msg("Sorry, there is already a player with the name '%s'." % playername)
            return
        # Verify that this player name does not match an existing character name
        for existing_object in search_object(playername, attribute_name='key'):
            if utils.inherits_from(existing_object, "src.objects.objects.Character"):
                session.msg("Sorry, there is already a character with the name '%s'." % playername)
                return
        # Security check the password
        if not re.findall('^[\w. @+-]+$', password) or not (3 < len(password)):
            string = "\n\r Password should be longer than 3 characers. Letters, spaces, digits and @\.\+\-\_ only."
            string += "\nFor best security, make it longer than 8 characters. You can also use a phrase of"
            string += "\nmany words if you enclose the password in quotes."
            session.msg(string)
            return

        # everything's ok. Create the new player account.
        try:
            default_home = ObjectDB.objects.get_id(settings.CHARACTER_DEFAULT_HOME)

            typeclass = settings.BASE_CHARACTER_TYPECLASS
            permissions = settings.PERMISSION_PLAYER_DEFAULT

            try:
                new_player = create.create_player(playername, None, password,
                                                     permissions=permissions)


            except Exception, e:
                session.msg("There was an error creating the default Player/Character:\n%s\n If this problem persists, contact an admin." % e)
                return

            # This needs to be called so the engine knows this player is logging in for the first time.
            # (so it knows to call the right hooks during login later)
            utils.init_new_player(new_player)

            # join the new player to the public channel
            pchanneldef = settings.CHANNEL_PUBLIC
            if pchanneldef:
                pchannel = Channel.objects.get_channel(pchanneldef[0])
                if not pchannel.connect_to(new_player):
                    string = "New player '%s' could not connect to public channel!" % new_player.key
                    logger.log_errmsg(string)


            # tell the caller everything went well.
            string = "A new account '%s' was created. Welcome!"
            if " " in playername:
                string += "\n\nYou can now log in with the command 'connect \"%s\" <your password>'."
            else:
                string += "\n\nYou can now log with the command 'connect %s <your password>'."
            session.msg(string % (playername, playername))

        except Exception:
            # We are in the middle between logged in and -not, so we have to handle tracebacks
            # ourselves at this point. If we don't, we won't see any errors at all.
            string = "%s\nThis is a bug. Please e-mail an admin if the problem persists."
            session.msg(string % (traceback.format_exc()))
            logger.log_errmsg(traceback.format_exc())

