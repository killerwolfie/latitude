from game.gamesrc.latitude.objects.exit import LatitudeExit

class LatitudeExitDeadbolt(LatitudeExit):
    def at_object_creation(self):
        super(LatitudeExitDeadbolt, self).at_object_creation()
	self.db.deadbolt_two_way = True
        self.locks.add("lock:all()")

    def action_unlock(self, unlocker):
        self.lock_unlock(unlocker, True)

    def action_lock(self, locker):
        self.lock_unlock(locker, False)

    def lock_unlock(self, locker, unlock):
        if not self.access(locker, 'lock'):
            locker.msg("You don't have the key to that lock.")
            return

	if unlock:
	    change_from = 'traverse:none()'
	    change_to = 'traverse:all()'
	    msg_already_done = 'That exit is already unlocked.'
	    msg_verb_tp = 'unlocks'
	    msg_verb_sp = 'unlock'
	else:
	    change_from = 'traverse:all()'
	    change_to = 'traverse:none()'
	    msg_already_done = 'That exit is already locked.'
	    msg_verb_tp = 'locks'
	    msg_verb_sp = 'lock'

	# Check the current traverse access
	current_lock = self.locks.get('traverse')

	if current_lock == change_to:
            locker.msg(msg_already_done)
	    return()

	if current_lock != change_from: # Unexpected traverse lock value
	    locker.msg('The lock appears to be jammed.')
	    return()

	if self.db.deadbolt_two_way:
            reverse_exits = list(exit for exit in self.reverse_exits() if isinstance(exit, LatitudeExitDeadbolt) and exit.db.deadbolt_two_way)

	    # Check the reverse exits to ensure they're in the proper state
	    # We don't care if the opposite side is already locked/unlocked.  This should force a sync.
	    for reverse_exit in reverse_exits:
	        reverse_lock = reverse_exit.locks.get('traverse')
		if reverse_lock != change_from and reverse_lock != change_to:
		    locker.msg('There seems to be a key broken off in the lock.')
		    return()

        # Apply lock
	exit_name = self.return_situational_name()
	
	if self.db.deadbolt_two_way:
	    for reverse_exit in reverse_exits:
	        reverse_exit.locks.add(change_to)
		# If we've gotten this far, the reverse exit must have a location.
		reverse_exit.location.msg_contents('%s %s %s from the other side.' % (locker.key, msg_verb_tp, exit_name), exclude=[locker])

	self.locks.add(change_to)
	if self.location:
	    self.location.msg_contents('%s %s %s.' % (locker.key, msg_verb_tp, exit_name), exclude=[locker])
	    locker.msg('You %s %s.' % (msg_verb_sp, exit_name))

    def at_failed_traverse(self, traversing_object):
        traversing_object.msg('Looks like that way is locked.')

    def at_failed_traverse_led(self, traversing_object):
        traversing_object.msg("You get left behind, because you can't make it through a locked exit.")
