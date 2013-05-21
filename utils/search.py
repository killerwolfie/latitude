"""
Search related functionality for Latitude
"""
from ev import utils
from src.players.models import PlayerDB
from src.objects.models import ObjectDB

def match_player(name):
    """
    This function is used to permit partial matching for players for convenience when parsing player commands.
    The following rules are used, in priority order:
      1) If the name is an exact match for a player, return the player.
      2) If the name is an exact match for a character, and there is a legitimate owning player (Which checks for the uniqueness of the character name), return it.
      3) If there is an unambiguous partial match with 'startswith', for either a player or character (with a legitimate owning player), and that player is online, return it.

    This configuration makes it impossible to reference a character which has a name which matches a player, but not its own.  This is because on Latitude, player and character names should never collide, and this sort of problem is to be expected if it does.  The 'get_owner()' routine should be checking to see if a character exists in this broken state, and returning None, making the system recognize it as an orphaned character.  Naturally, this requires the command which creates new player accounts to carefully check for existing character names!
    """
    # Check for exact player matches
    matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__iexact=name)]
    if matching_players:
        return matching_players[0]
    # Check for exact character matches
    matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__iexact=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character")]
    if matching_characters:
        for matching_character in matching_characters:
            matching_player = matching_character.get_owner() # This should return None in the case of a duplicate character name, so we don't have to check for that.
            if matching_player:
                return matching_player
    # Check for inexact matches
    matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__istartswith=name)]
    matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__istartswith=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character")]
    if len(matching_players + matching_characters) != 1:
        # Ambiguous match
        return None
    if matching_players:
        return matching_players[0]
    return matching_characters[0].get_owner()
