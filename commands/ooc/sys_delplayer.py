from ev import default_cmds

class CmdSysDelPlayer(default_cmds.CmdDelPlayer):
    """
    delplayer - delete player from server

    Usage:
      @delplayer[/switch] <name> [: reason]

    Switch:
      delobj - also delete the player's currently
               assigned in-game object.

    Completely deletes a user from the server database,
    making their nick and e-mail again available.
    """

    key = "@delplayer"
    locks = "cmd:perm(delplayer) or perm(Immortals)"
    help_category = "Admin"

