from ev import default_cmds

class CmdSysBan(default_cmds.CmdBan):
    """
    ban a player from the server

    Usage:
      @ban [<name or ip> [: reason]]

    Without any arguments, shows numbered list of active bans.

    This command bans a user from accessing the game. Supply an
    optional reason to be able to later remember why the ban was put in
    place

    It is often to
    prefer over deleting a player with @delplayer. If banned by name,
    that player account can no longer be logged into.

    IP (Internet Protocol) address banning allows to block all access
    from a specific address or subnet. Use the asterisk (*) as a
    wildcard.

    Examples:
      @ban thomas             - ban account 'thomas'
      @ban/ip 134.233.2.111   - ban specific ip address
      @ban/ip 134.233.2.*     - ban all in a subnet
      @ban/ip 134.233.*.*     - even wider ban

    A single IP filter is easy to circumvent by changing the computer
    (also, some ISPs assign only temporary IPs to their users in the
    first placer. Widening the IP block filter with wildcards might be
    tempting, but remember that blocking too much may accidentally
    also block innocent users connecting from the same country and
    region.

    """
    key = "@ban"
    locks = "cmd:perm(command_@ban) or perm(Janitors)"
    help_category="=== Admin ==="

