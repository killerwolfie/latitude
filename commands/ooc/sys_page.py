from ev import default_cmds

class CmdSysPage(default_cmds.CmdPage):
    """
    page - send private message

    Usage:
      page[/switches] [<player>,<player>,... = <message>]
      tell        ''
      page <number>

    Switch:
      last - shows who you last messaged
      list - show your last <number> of tells/pages (default)

    Send a message to target user (if online). If no
    argument is given, you will get a list of your latest messages.
    """

    key = "page"
    aliases = ['tell']
    locks = "cmd:not pperm(page_banned)"
    help_category = "Comms"

