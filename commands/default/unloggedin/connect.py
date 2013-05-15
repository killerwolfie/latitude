"""
Commands that are available from the connect screen.
"""
import re
import traceback
import shlex
from src.players.models import PlayerDB
from src.server.models import ServerConfig

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
        parts = [part.strip() for part in re.split(r"\"|\'", args) if part.strip()]
        if len(parts) == 1:
            # this was (hopefully) due to no quotes being found
            parts = parts[0].split(None, 1)
        if len(parts) != 2:
            session.msg("\n\r Usage (without <>): connect <name> <password>")
            return
        playername, password = parts

        # Match account name and check password
        player = PlayerDB.objects.get_player_from_name(playername)
        pswd = None
        if player:
            pswd = player.user.check_password(password)

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

        # actually do the login. This will call all other hooks:
        #   session.at_login()
        #   player.at_init()         # always called when object is loaded from disk
        #   player.at_pre_login()
        #   player.at_first_login()  # only once
        #   player.at_post_login(sessid=sessid)
        session.sessionhandler.login(session, player)
