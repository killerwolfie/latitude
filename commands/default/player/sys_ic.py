from ev import default_cmds
from src.utils import search

class CmdSysIC(default_cmds.MuxPlayerCommand):
    """
    Switch control to an object

    Usage:
      @ic <character>

    Go in-character (IC) as a given Character.

    This will attempt to "become" a different object assuming you have
    the right to do so. Note that it's the PLAYER character that puppets
    characters/objects and which needs to have the correct permission!

    You cannot become an object that is already controlled by another
    player. In principle <character> can be any in-game object as long
    as you the player have access right to puppet it.
    """

    key = "@ic"
    locks = "cmd:all()" # must be all() or different puppeted objects won't be able to access it.
    aliases = "@puppet"
    help_category = "General"

    def func(self):
        """
        Main puppet method
        """
        player = self.caller
        sessid = self.sessid
        anyobj = 'anyobj' in [switch.lower() for switch in self.switches]

        new_character = None
        if not self.args:
            new_character = player.db._last_puppet
            if not new_character:
                # Trying to become @ic without specifying a character
                if player.get_puppet(sessid):
                    self.msg("Usage: @ic <character>")
                else:
                    # We're currently OOC.  Perform an OOC look instead, so the user can see the character select / account management menu.
                    player.execute_cmd("look", sessid=sessid)
                return
        if not new_character:
            if player.db._playable_characters:
                # Search through your list of characters first
                for playable_character in player.db._playable_characters:
                    if self.args.lower() == playable_character.key.lower():
                        new_character = playable_character
                        break
        if not new_character:
            if anyobj:
                # search for a matching character
                new_character = search.object_search(self.args)
                if new_character:
                    new_character = new_character[0]
                else:
                    self.msg("That is not a valid character choice.")
                    return
            else:
                self.msg("That's not one of your playable characters.")
                return
        # permission checks
        if player.get_puppet(sessid) == new_character:
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
        if player.puppet_object(sessid, new_character):
            player.db._last_puppet = new_character
            if not new_character.location:
                # this might be due to being hidden away at logout; check
                loc = new_character.db.prelogout_location
                if not loc: # still no location; use home
                    loc = new_character.home
                new_character.location = loc
                new_character.location.at_object_receive(new_character, new_character.location)
        else:
            self.msg("{rYou cannot become {C%s{n." % new_character.name)

