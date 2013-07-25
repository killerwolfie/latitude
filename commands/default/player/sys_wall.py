from src.server.sessionhandler import SESSIONS
from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand

class CmdSysWall(LatitudeCommand):
    """
    @wall - Send a message to all connected players

    Usage:
      @wall <message>
        Sends a message to all connected players.
    """
    key = "@wall"
    locks = "cmd:perm(command_@wall) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"
    logged = True

    def func(self):
        player = self.player
        character = self.character
        # Check arguments
        message = self.args
        if not message:
            self.msg("{R[Invalid '{r%s{R' command.  See '{rhelp %s{R' for usage]" % (self.cmdstring, self.key))
            return
        # Format the message
        if character:
            # If we have a character, then we can use the 'say' routines to format the message.
            if message.startswith(':'):
                message = character.speech_pose(message[1:])
            elif message.startswith('"'):
                message = character.speech_say(message[1:])
            else:
                message = character.speech_say(message)
        else:
            # If we have no character, we'll have to take care of the formatting
            if message.startswith(':'):
                message = '{b' + player.key + '{n ' + message[1:].replace('{', '{{').replace('%', '%%')
            elif message.startswith('"'):
                message = '{b' + player.key + '{n: ' + message[1:].replace('{', '{{').replace('%', '%%')
            else:
                message = '{b' + player.key + '{n: ' + message.replace('{', '{{').replace('%', '%%')
        message = "{Y[ {cShout {Y| {n%s {Y]" % (message)
        # Send it
        for session in SESSIONS.get_sessions():
            session_sessid = session.sessid
            session_player = session.get_player()
            if not session_player:
                continue
            session_player.msg(message, sessid=session_sessid)
