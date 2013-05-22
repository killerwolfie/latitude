"""
Search related functionality for Latitude
"""
from ev import utils
from src.players.models import PlayerDB
from src.objects.models import ObjectDB

def match_player(name, exact=False):
    """
    This function is used to permit partial matching for players for convenience when parsing player commands.
    The following rules are used, in priority order:
      1) If the name is an exact match for a player, return the player.
      2) If the name is an exact match for a character, and there is a legitimate owning player (Which checks for the uniqueness of the character name), return it.
      3) If there is an unambiguous partial match with 'startswith', for either a player or character (with a legitimate owning player), and that player is online, return it.

    This configuration makes it impossible to reference a character which has a name which matches a player, but not its own.  This is because on Latitude, player and character names should never collide, and this sort of problem is to be expected if it does.  The 'get_owner()' routine should be checking to see if a character exists in this broken state, and returning None, making the system recognize it as an orphaned character.  Naturally, this requires the command which creates new player accounts to carefully check for existing character names!

    Also, you can ambiguously match a character and a player, so long as every possible match is the same player.
    """
    # Check for exact player matches
    matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__iexact=name)]
    if matching_players:
        return matching_players[0]
    # Check for exact character matches
    matching_players = [match.typeclass.get_owner() for match in ObjectDB.objects.filter(db_key__iexact=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.get_owner()]
    if matching_players:
        return matching_players[0]
    # Check for inexact matches
    if not exact:
        matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__istartswith=name)]
        matching_players += [match.typeclass.get_owner() for match in ObjectDB.objects.filter(db_key__istartswith=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.get_owner()]
        if len(set(matching_players)) == 1: # Results must be unambiguous
            return matching_players[0]
    # No matches
    return None

def match_character(name, exact=False):
    """
    Like match_player, only it only returns characters.
    """
    # Check for exact character matches
    matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__iexact=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.get_owner()]
    if matching_characters:
        return matching_characters[0]
    # Check for inexact matches
    if not exact:
        matching_players = [match.typeclass for match in ObjectDB.objects.filter(db_key__istartswith=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.get_owner()]
        if len(set(matching_players)) == 1: # Results must be unambiguous
            return matching_players[0]
    # No matches
    return None
