from ev import Command, CmdSet

class CmdMenu(Command):
    locks = "cmd:all()"
    def __init__(self, key, aliases=[], menustring=None):
        super(CmdMenu, self).__init__()
        self.key = key
        self.aliases = aliases
        self.menustring = menustring

class CmdMenuGoto(CmdMenu):
    locks = "cmd:all()"

    def __init__(self, key, node, aliases=[], menustring=None):
        super(CmdMenuGoto, self).__init__(key=key, aliases=aliases, menustring=menustring)
        self.node = node

    def func(self):
        self.menutree.goto(self.node)

class CmdMenuCode(CmdMenu):
    locks = "cmd:all()"

    def __init__(self, key, code, aliases=[], menustring=None):
        super(CmdMenuCode, self).__init__(key=key, aliases=aliases, menustring=menustring)
        self.code = code

    def func(self):
        try:
            exec(self.code)
        except Exception, e:
            self.caller.msg("%s\n{rThere was an error with this selection." % e)

class CmdMenuList(CmdMenu):
    locks = "cmd:all()"

    def __init__(self, key, top_msg, aliases=[], menustring=None):
        super(CmdMenuList, self).__init__(key=key, aliases=aliases, menustring=menustring)
        self.top_msg = top_msg

    def func(self):
        self.caller.msg(self.top_msg)
        for cmd in self.menutree.current_node:
            if cmd.menustring:
                self.caller.msg('%s - %s' % (cmd.key, cmd.menustring))

class CmdsetMenu(CmdSet):
    key = "menucmdset"
    priority = 1
    mergetype = "Replace"
    def at_cmdset_creation(self):
        pass

class MenuTree(object):
    def __init__(self, caller, nodes, refresh_cmd='look'):
        self.caller = caller
        self.nodes = nodes
        self.refresh_cmd = refresh_cmd
        for node in nodes.values():
            for cmd in node:
                cmd.menutree = self

    def goto(self, node):
        # Delete the old cmdset
        self.caller.cmdset.delete("menucmdset")
        # Produce a new cmdset to add, if any
        if node:
            if not node in self.nodes:
                self.caller.msg("{rMenu entry not found!  Exiting.")
                self.current_node = None
                return
            self.current_node = self.nodes[node]
            # Create and add a new cmdset for a new menu entry
            menucmdset = CmdsetMenu()
            for cmd in self.current_node:
                menucmdset.add(cmd)
            self.caller.cmdset.add(menucmdset)
        else:
            self.current_node = None
        # Call the refresh command.  It's called even if the menu has exited.
        self.refresh()

    def refresh(self):
        # Issue the desired refresh command to display the menu entry to the user
        self.caller.execute_cmd(self.refresh_cmd)

class CmdMenuTest(Command):
    """
    menu testing command

    Usage:
        menu
    """
    key = "menu"
    locks = "cmd:all()"
    help_category = "Menu"

    def func(self):
        "Testing the menu system"
        menu = MenuTree(self.caller, nodes={
            'node0' : [
                CmdMenuList(key='look', aliases=['help'], top_msg='Start node. Select one of the links below. Here the links are ordered in one column.'),
                CmdMenuGoto(key='1', menustring='Goto first node', node='node1'),
                CmdMenuGoto(key='2', menustring='Goto second node', node='node2'),
                CmdMenuGoto(key='3', menustring='Quit', node=None),
            ],
            'node1' : [
                CmdMenuList(key='look', aliases=['help'], top_msg='First node.  This node shows letters instead of numbers for the choices.'),
                CmdMenuGoto(key='q', menustring='Quit', node=None),
                CmdMenuGoto(key='b', menustring='Back to start', node='node0'),
            ],
            'node2' : [
                CmdMenuList(key='look', aliases=['help'], top_msg='Second node.  This node lists choices in two columns.'),
                CmdMenuCode(key='1', menustring='Set menutest attribute', code='self.caller.db.menutest="Testing!"; self.caller.msg("Attribute \'menutest\' set on you.  If you examine yourself, you can see it."); self.menutree.refresh()'),
                CmdMenuCode(key='2', menustring='Examine yourself', code='self.caller.msg("%s/%s = %s" % (self.caller.key, \'menutest\', self.caller.db.menutest)); self.menutree.refresh()'),
                CmdMenuGoto(key='3', menustring='Quit', node=None),
                CmdMenuCode(key='4', menustring='Remove attribute and quit', code='del self.caller.db.menutest; self.menutree.goto(None)'),
            ],
        })
        menu.goto('node0') # Start the menu

