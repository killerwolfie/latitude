from ev import default_cmds

class CmdSysBoot(default_cmds.CmdBoot):
    """
    @boot

    Usage
      @boot[/switches] <player obj> [: reason]

    Switches:
      quiet - Silently boot without informing player
      port - boot by port number instead of name or dbref

    Boot a player object from the server. If a reason is
    supplied it will be echoed to the user unless /quiet is set.
    """

    key = "@boot"
    aliases = []
    locks = "cmd:pperm(boot) or pperm(Janitors)"
    help_category = "=== Admin ==="

    def func(self):
        "Implementing the function"
        caller = self.caller
        args = self.args

        if not args:
            caller.msg("Usage: @boot[/switches] <player> [:reason]")
            return

        if ':' in args:
            args, reason = [a.strip() for a in args.split(':', 1)]
        else:
            args, reason = args, ""

        boot_list = []

        if 'port' in self.switches:
            # Boot a particular port.
            sessions = SESSIONS.get_session_list(True)
            for sess in sessions:
                # Find the session with the matching port number.
                if sess.getClientAddress()[1] == int(args):
                    boot_list.append(sess)
                    break
        else:
            # Boot by player object
            pobj = search.player_search(args)
            if not pobj:
                self.caller("Player %s was not found." % pobj.key)
                return
            pobj = pobj[0]
            # we have a bootable object with a connected user
            matches = SESSIONS.sessions_from_player(pobj)
            for match in matches:
                boot_list.append(match)

        if not boot_list:
            caller.msg("No matching sessions found. The Player does not seem to be online.")
            return

        # Carry out the booting of the sessions in the boot list.

        feedback = None
        if not 'quiet' in self.switches:
            feedback = "You have been disconnected by %s.\n" % caller.name
            if reason:
                feedback += "\nReason given: %s" % reason

        for session in boot_list:
            session.msg(feedback)
            pobj.disconnect_session_from_player(session.sessid)
