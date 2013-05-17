from ev import default_cmds

class CmdSysDelPlayer(default_cmds.MuxCommand):
    """
    @delplayer - delete player from server

    Usage:
      @delplayer[/switch] <name> [: reason]

    Switch:
      delobj - also delete the player's currently
               assigned in-game object.

    Completely deletes a user from the server database,
    making their nick and e-mail again available.
    """

    key = "@delplayer"
    locks = "cmd:pperm(command_delplayer) or pperm(Janitors)"
    help_category = "=== Admin ==="

    def func(self):
        "Implements the command."

        caller = self.caller
        args = self.args

        if hasattr(caller, 'player'):
            caller = caller.player

        if not args:
            self.msg("Usage: @delplayer[/delobj] <player/user name or #id> [: reason]")
            return

        reason = ""
        if ':' in args:
            args, reason = [arg.strip() for arg in args.split(':', 1)]

        # We use player_search since we want to be sure to find also players
        # that lack characters.
        players = caller.search_player(args, quiet=True)

        if not players:
            # try to find a user instead of a Player
            try:
                user = User.objects.get(id=args)
            except Exception:
                try:
                    user = User.objects.get(username__iexact=args)
                except Exception:
                    string = "No Player nor User found matching '%s'." % args
                    self.msg(string)
                    return
            try:
                player = user.get_profile()
            except Exception:
                player = None

            string = ""
            name = user.username
            user.delete()
            if player:
                name = player.name
                player.delete()
                string = "Player %s was deleted." % name
            else:
                string += "The User %s was deleted. It had no Player associated with it." % name
            self.msg(string)
            return

        elif utils.is_iter(players):
            string = "There were multiple matches:"
            for player in players:
                string += "\n %s %s" % (player.id, player.key)
            return
        else:
            # one single match

            player = players
            user = player.user

            uname = user.username
            # boot the player then delete
            self.msg("Informing and disconnecting player ...")
            string = "\nYour account '%s' is being *permanently* deleted.\n" %  uname
            if reason:
                string += " Reason given:\n  '%s'" % reason
            player.unpuppet_all()
            for session in SESSIONS.sessions_from_player(player):
                player.msg(string, sessid=session.sessid)
                player.disconnect_session_from_player(session.sessid)
            user.delete()
            player.delete()
            self.msg("Player %s was successfully deleted." % uname)

