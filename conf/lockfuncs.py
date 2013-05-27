from ev import utils
from game.gamesrc.latitude.objects.room import LatitudeRoom

def resident(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Used in a lockstring as resident() to determine if the accessed_obj is
    within a residence of the accessing_obj.
    It works by ascending the object tree until it hits a room, then checking
    the 'resident' attribute of the room.
    It returns True only if the attribute is set, and there is a match.
    """
    room = accessed_obj
    while not isinstance(room.typeclass, LatitudeRoom):
        if not room.location:
	    return False
	room = room.location

    return(accessing_obj == room.db.resident)

def deadbolt_key(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
      deadbolt_key(keypass)

    Passes if this object, or any of its contents, recursively, have a serial code matching the value supplied in 'keypass'.
    The deadbolt key value is a list of serial codes, stored as the attribute 'deadbolt_key'
    """
    if not args or not len(args) == 1:
        return False
    try:
        if accessing_obj.db.deadbolt_key and args[0] in accessing_obj.db.deadbolt_key:
            return True
        for child in accessing_obj.contents:
            if deadbolt_key(child, accessed_obj, args[0]):
                return True
    except TypeError:
        return False
    return False

def owner_lock(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
      owner_lock(lockname)

    Passes this check on to the owner object.

    Returns False if not run on an object which has the get_owner() method.
    """
    if not args or not len(args) == 1:
        return False
    if not hasattr(accessed_obj, 'get_owner'):
        return False
    owner = accessed_obj.get_owner()
    if not owner or not utils.inherits_from(owner, 'src.players.player.Player'):
        return False
    return owner.access(accessing_obj, args[0])

def friend(accessing_obj, accessed_obj, *args, **kwargs):
    """
    Usage:
        friend()

    Returns True if the accessing_obj and accessed_obj are friends in the @friend system.
    If they objects are not players, it checks for a get_owner() method, and uses their owner player if available.
    """
    accessing_obj = accessing_obj.typeclass
    accessed_obj = accessed_obj.typeclass
    if not utils.inherits_from(accessing_obj, 'src.players.player.Player'):
        if not hasattr(accessing_obj, 'get_owner'):
            return False
        accessing_obj = accessing_obj.get_owner()
    if not utils.inherits_from(accessed_obj, 'src.players.player.Player'):
        if not hasattr(accessed_obj, 'get_owner'):
            return False
        accessed_obj = accessed_obj.get_owner()
    return accessing_obj in accessed_obj.get_friend_players()
