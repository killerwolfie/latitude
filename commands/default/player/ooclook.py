from game.gamesrc.latitude.commands.default.character import look
from src.commands.default.muxcommand import MuxPlayerCommand
from ev import default_cmds
from ev import utils

class CmdOOCLook(MuxPlayerCommand):
    """
    ooc look

    Usage:
      look

    This is an OOC version of the look command. Since a
    Player doesn't have an in-game existence, there is no
    concept of location or "self". If we are controlling
    a character, pass control over to normal look.

    """

    key = "look"
    aliases = []
    locks = "cmd:all()"
    help_category = "Actions"

    def look_target(self):
        "Hook method for when an argument is given."
        player = self.caller
        key = self.args.lower()
        chars = dict((utils.to_str(char.key.lower()), char) for char in player.db._playable_characters)
        looktarget = chars.get(key)
        if looktarget:
            self.msg(looktarget.return_appearance(player))
        else:
            self.msg("No such character.")
        return

    def no_look_target(self):
        "Hook method for default look without a specified target"
        # caller is always a player at this point.
        player = self.caller
        sessid = self.sessid
        # get all our characters and sessions
        characters = player.db._playable_characters
        sessions = player.get_all_sessions()

        # text shown when looking in the ooc area
        string = "Account {g%s{n (you are Out-of-Character)" % (player.key)

        nsess = len(sessions)
        string += nsess == 1 and "\n\n{wConnected session:{n" or "\n\n{wConnected sessions (%i):{n" % nsess
        for isess, sess in enumerate(sessions):
            csessid = sess.sessid
            addr = "%s (%s)" % (sess.protocol_key, isinstance(sess.address, tuple) and str(sess.address[0]) or str(sess.address))
            string += "\n %s %s" % (sessid == csessid and "{w%s{n" % (isess + 1) or (isess + 1), addr)
        string += "\n\n {whelp{n - more commands"
        string += "\n {wpub <Text>{n - talk on public channel"

        max_characters = player.max_characters()
        if len(characters) < max_characters:
            if not characters:
                string += "\n\n You don't have any character yet. See {whelp @charcreate{n for creating one."
            else:
                string += "\n {w@charcreate <name> [=description]{n - create new character"

        if characters:
            string_s_ending = len(characters) > 1 and "s" or ""
            string += "\n {w@ic <character>{n - enter the game ({w@ooc{n to get back here)"
            string += "\n\nAvailable character%s%s:"  % (string_s_ending, max_characters > 1 and ' (' + str(len(characters)) + '/' + str(max_characters) + ')')

            for char in characters:
                csessid = char.sessid
                if csessid:
                    # character is already puppeted
                    sess = player.get_session(csessid)
                    if sess:
                        sid = sess in sessions and sessions.index(sess) + 1
                        string += "\n - {G%s{n (played by you in session %i)" % (char.key, sid)
                    else:
                        string += "\n - {R%s{n (played by someone else)" % (char.key)
                else:
                    # character is "free to puppet"
                    string += "\n - %s" % (char.key)
        string = ("-" * 68) + "\n" + string + "\n" + ("-" * 68)
        self.msg(string)

    def func(self):
        "implement the ooc look command"
        if utils.inherits_from(self.caller, "src.objects.objects.Object"):
            # An object of some type is calling. Use default look instead.
            super(CmdOOCLook, self).func()
        elif self.args:
            self.look_target()
        else:
            self.no_look_target()

