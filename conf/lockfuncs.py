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
   if not args:
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
