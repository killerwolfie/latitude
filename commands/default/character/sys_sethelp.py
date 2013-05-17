from ev import default_cmds

class CmdSysSetHelp(default_cmds.CmdSetHelp):
    """
    @help - edit the help database

    Usage:
      @help[/switches] <topic>[,category[,locks]] = <text>

    Switches:
      add    - add or replace a new topic with text.
      append - add text to the end of topic with a newline between.
      merge  - As append, but don't add a newline between the old
               text and the appended text.
      delete - remove help topic.
      force  - (used with add) create help topic also if the topic
               already exists.

    Examples:
      @sethelp/add throw = This throws something at ...
      @sethelp/append pickpocketing,Thievery = This steals ...
      @sethelp/append pickpocketing, ,attr(is_thief) = This steals ...

    This command manipulates the help database. A help entry can be created,
    appended/merged to and deleted. If you don't assign a category, the "General"
    category will be used. If no lockstring is specified, default is to let everyone read
    the help file.

    """
    key = "@sethelp"
    aliases = []
    locks = "cmd:perm(command_@sethelp) or pperm(Custodians)"
    help_category = "--- Coder/Sysadmin ---"

