"""
Search related functionality for Latitude
"""
from ev import utils
from src.players.models import PlayerDB
from src.objects.models import ObjectDB

def match(name, exact=False):
    """
    This function is used to permit partial matching for players/characters for convenience when parsing player commands.
    The following rules are used, in priority order:
      1) If the name is an exact match for a character, and there is a legitimate owning player (Which checks for the uniqueness of the character name), return it.
      2) If the name is an exact match for a player, return the player.
      3) If there is an unambiguous partial match with 'startswith', for either a player or character (with a legitimate owning player), and that player is online, return it.

    This configuration makes it impossible to reference a character which has a name which matches a player, but not its own.  This is because on Latitude, player and character names should never collide, and this sort of problem is to be expected if it does.  The 'get_owner()' routine should be checking to see if a character exists in this broken state, and returning None, making the system recognize it as an orphaned character.  Naturally, this requires the command which creates new player accounts to carefully check for existing character names!

    Also, you can ambiguously match a character and a player, so long as every possible match is the same player.
    """
    # Don't bother with blank names
    if not name:
        return None
    # Check for exact character matches
    matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__iexact=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.get_owner()]
    if matching_characters:
        return matching_characters[0]
    # Check for exact player matches
    matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__iexact=name)]
    if matching_players:
        return matching_players[0]
    # Check online users for inexact matches
    if not exact:
        matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__istartswith=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.sessid and match.typeclass.get_owner()]
        matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__istartswith=name) if match.typeclass.sessions]
        # Check for unambiguous character match
        if len(matching_characters) == 1 and not matching_players:
            return matching_characters[0]
        # Check for unambiguous player match
        if len(matching_players) == 1 and not matching_characters:
            return matching_players[0]
        # Check for unambiguous match of a character and player with exactly the same name
        if len(matching_players) == 1 and len(matching_characters) == 1:
            if matching_players[0].key.lower() == matching_characters[0].key.lower() and matching_players[0] == matching_characters[0].get_owner():
                # Player has the same name as character.  Return character.
                return matching_characters[0]
    # No matches
    return None

def match_player(name, exact=False):
    """
    Like match, only it only returns players, and specifying a name which could also ambiguously reference a character name doesn't cause a problem.
    
    For example:
      Character: Blazing Saddles
      Player: Blaze
      Search: Blaz
      Result: Blaze
      (match() would return None)
    """
    # Don't bother with blank names
    if not name:
        return None
    # Check for exact player matches
    matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__iexact=name)]
    if matching_players:
        return matching_players[0]
    # Check for inexact matches
    if not exact:
        matching_players = [match.typeclass for match in PlayerDB.objects.filter(user__username__istartswith=name) if match.typeclass.sessions]
        # Check for unambiguous player match
        if len(matching_players) == 1:
            return matching_players[0]
    # No matches
    return None

def match_character(name, exact=False):
    """
    Like match, only it only returns characters, and specifying a name which could also ambiguously reference a player name doesn't cause a problem.

    For example:
      Character: Blazing Saddles
      Player: Blaze
      Search: Blaz
      Result: Blazing Saddles
      (match() would return None)
    """
    # Don't bother with blank names
    if not name:
        return None
    # Check for exact character matches
    matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__iexact=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.get_owner()]
    if matching_characters:
        return matching_characters[0]
    # Check for inexact matches
    if not exact:
        matching_characters = [match.typeclass for match in ObjectDB.objects.filter(db_key__istartswith=name) if utils.inherits_from(match.typeclass, "src.objects.objects.Character") and match.typeclass.sessid and match.typeclass.get_owner()]
        if len(set(matching_characters)) == 1: # Results must be unambiguous
            return matching_characters[0]
    # No matches
    return None

