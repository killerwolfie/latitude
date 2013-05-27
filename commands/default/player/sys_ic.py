from ev import default_cmds
from src.utils import search
from ev import settings

class CmdSysIC(default_cmds.MuxPlayerCommand):
    """
    Switch control to an object

    Usage:
      @ic <character>

    Go in-character (IC) as a given Character.  This is how you 'become' a given character from the list of characters associated with your account.
    """

    key = "@ic"
    locks = "cmd:all()" # must be all() or different puppeted objects won't be able to access it.
    aliases = []
    help_category = "General"
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        player = self.caller
        playable_characters = self.caller.get_playable_characters()
        # Determine which character to occupy
        if self.args:
            for character in playable_characters:
                if self.args.lower() == character.key.lower():
                    self.puppet(character)
                    return
            self.msg('That is not a valid character selection.')
        else:
            if player.db._last_puppet and player.db._last_puppet in playable_characters:
                self.puppet(player.db._last_puppet)
                return
            else:
                # Trying to become @ic without specifying a character
                if player.get_puppet(self.sessid):
                    self.msg("Usage: @ic <character>")
                else:
                    # We're currently OOC.  Perform an OOC look instead, so the user can see the character select / account management menu.
                    player.execute_cmd("look", sessid=self.sessid)
                return

    def puppet(self, new_character):
        player = self.caller
        # permission checks
        if player.get_puppet(self.sessid) == new_character:
            self.msg("{RYou already act as {c%s{n." % new_character.name)
            return
        if new_character.player:
            # may not puppet an already puppeted character
            if new_character.sessid and new_character.player == player:
                # as a safeguard we allow "taking over chars from your own sessions.
                player.msg("{c%s{n{R is now acted from another of your sessions.{n" % (new_character.name), sessid=new_character.sessid)
                player.unpuppet_object(new_character.sessid)
                self.msg("Taking over {c%s{n from another of your sessions." % new_character.name)
            elif new_character.player != player and new_character.player.is_connected:
                self.msg("{c%s{r is already acted by another player.{n" % new_character.name)
                return
        if not new_character.access(player, "puppet"):
            # main acccess check
            self.msg("{rYou may not become %s.{n" % new_character.name)
            return
        if player.puppet_object(self.sessid, new_character):
            player.db._last_puppet = new_character
            if not new_character.location:
                new_character.location = new_character.db.home
                new_character.location.at_object_receive(new_character, new_character.location)
        else:
            self.msg("{rYou cannot become {C%s{n." % new_character.name)

