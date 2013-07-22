"""
Commands that are available from the connect screen.
"""
import re
import traceback
import shlex
from src.players.models import PlayerDB
from src.server.models import ServerConfig
from src.utils import search

from src.commands.default.muxcommand import MuxCommand

class CmdUnconnectedConnect(MuxCommand):
    """
    Connect to the game.

    Usage (at login screen):
      connect playername password
      connect "player name" "pass word"

    Use the create command to first create an account before logging in.

    If you have spaces in your name, enclose it in quotes.
    """
    key = "connect"
    aliases = ["conn", "con", "co"]
    locks = "cmd:all()" # not really needed

    def func(self):
        """
        Uses the Django admin api. Note that unlogged-in commands
        have a unique position in that their func() receives
        a session object instead of a source_object like all
        other types of logged-in commands (this is because
        there is no object yet before the player has logged in)
        """

        session = self.caller
        args = self.args
        # extract quoted parts
        parts = shlex.split(args)
        if len(parts) == 2:
            playername = parts[0]
            password = parts[1]
            # Check for | syntax
            username_parts = playername.split('|')
            if len(username_parts) == 2:
                playername = username_parts[0]
                charname = username_parts[1]
            else:
                charname = None
        else:
            session.msg("\n\r Usage (without <>): connect <username> <password>, or connect <username>|<character> <password>")
            return

        # Match account name and check password
        player = PlayerDB.objects.get_player_from_name(playername)
        pswd = None
        if player:
            pswd = player.user.check_password(password)
#            pswd = player.check_password(password) # FIXME-UPDATE

        if not (player and pswd):
        # No playername or password match
            string = "Wrong login information given.\nIf you have spaces in your name or "
            string += "password, don't forget to enclose it in quotes. Also capitalization matters."
            string += "\nIf you are new you should first create a new account "
            string += "using the 'create' command."
            session.msg(string)
            return

        # Check IP and/or name bans
        bans = ServerConfig.objects.conf("server_bans")
        if bans and (any(tup[0]==player.name for tup in bans)
                     or
                     any(tup[2].match(session.address[0]) for tup in bans if tup[2])):
            # this is a banned IP or name!
            string = "{rYou have been banned and cannot continue from here."
            string += "\nIf you feel this ban is in error, please email an admin.{x"
            session.msg(string)
            session.execute_cmd("quit")
            return

        # If they've requested a character name, verify that they have puppet access.
        if charname:
            character = search.object_search(charname)
            if not character:
                session.msg("{rThat character name doesn't appear to be valid.{x")
                return
            character = character[0]
            if not character.access(player, "puppet"):
                string = "{rThat does not appear to be one of your characters.  Try logging in\n"
                string += "without specifying a character name, and examine your list of available\n"
                string += "characters.{x"
                session.msg(string)
                return
        else:
            character = None

        # actually do the login. This will call all other hooks:
        #   session.at_login()
        #   player.at_init()         # always called when object is loaded from disk
        #   player.at_pre_login()
        #   player.at_first_login()  # only once
        #   player.at_post_login(sessid=sessid)
        session.sessionhandler.login(session, player)

        # Now that we're connected, puppet the character, if requested.
        if character:
            session.msg('\n{WLogging directly into {c%s{W...\n' % (character.get_desc_styled_name(player)))
            player.do_puppet(session.sessid, character)
