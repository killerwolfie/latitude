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
