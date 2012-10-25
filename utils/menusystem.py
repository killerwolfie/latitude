from ev import Command, CmdSet

class CmdMenuGoto(Command):
    locks = "cmd:all()"

    def __init__(self, key, node, aliases=[], menustring=None):
        super(CmdMenuGoto, self).__init__()
        self.key = key
        self.aliases = aliases
        self.menustring = menustring
        self.node = node

    def func(self):
        if not hasattr(self, 'menutree'):
            self.caller.msg('{rThis command is intended to be called from the dbmenu system.')
            return
        self.menutree.goto(self.node)
        self.menutree.refresh()

class CmdMenuQuit(Command):
    """
    Ends the associated menutree, and runs the 'look' command.
    """
    locks = "cmd:all()"

    def __init__(self, key, aliases=[], menustring=None):
        super(CmdMenuQuit, self).__init__()
        self.key = key
        self.aliases = aliases
        self.menustring = menustring

    def func(self):
        if not hasattr(self, 'menutree'):
            self.caller.msg('{rThis command is intended to be called from the dbmenu system.')
            return
        self.menutree.end()
        self.caller.execute_cmd('look')

class CmdMenuCode(Command):
    locks = "cmd:all()"

    def __init__(self, key, code, aliases=[], menustring=None):
        super(CmdMenuCode, self).__init__()
        self.key = key
        self.aliases = aliases
        self.menustring = menustring
        self.code = code

    def func(self):
        if not hasattr(self, 'menutree'):
            self.caller.msg('{rThis command is intended to be called from the dbmenu system.')
            return
        try:
            exec(self.code)
        except Exception, e:
            self.caller.msg("%s\n{rThere was an error with this selection." % e)
        self.menutree.refresh()

class CmdsetMenu(CmdSet):
    key = "menucmdset"
    priority = 1
    mergetype = "Replace"
    def at_cmdset_creation(self):
        pass

class MenuNode(object):
    def __init__(self, cmds, text=None, cols=1):
        self.cmds = cmds
        self.text = text
        self.cols = 1

    def init(self, menutree):
        self.cmdset = CmdsetMenu()
        for cmd in self.cmds:
            cmd.menutree = menutree
            self.cmdset.add(cmd)
            if cmd.menustring:
                # TODO: Columns
                self.text += '\n%s - %s' % (cmd.key, cmd.menustring)
         

class MenuTree(object):
    def __init__(self, caller, nodes):
        self.caller = caller
        self.nodes = nodes
        self.current_node = None
        for node in nodes.values():
            node.init(self)

    def goto(self, node):
        if not node in self.nodes:
            self.caller.msg("{rThe requested menu node is not defined.  Perhaps it hasn't been created yet?")
        # Delete the old cmdset
        self.caller.cmdset.delete("menucmdset")
        # Set the new current node, display its text, and assign its cmdset to the user
        self.current_node = self.nodes[node]
        self.caller.msg(self.current_node.text)
        self.caller.cmdset.add(self.current_node.cmdset)

    def end(self):
        self.caller.cmdset.delete("menucmdset")
        self.current_node = None

    def refresh(self):
        if self.current_node:
            self.caller.msg(self.current_node.text)

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
            'node0' : MenuNode(text="Start node. Select one of the links below. Here the links are ordered in one column.", cmds=[
                CmdMenuGoto(key='1', menustring='Goto first node', node='node1'),
                CmdMenuGoto(key='2', menustring='Goto second node', node='node2'),
                CmdMenuQuit(key='3', menustring='Quit'),
            ]),
            'node1' : MenuNode(text="First node.  This node shows letters instead of numbers for the choices.", cols=2, cmds=[
                CmdMenuQuit(key='q', menustring='Quit'),
                CmdMenuGoto(key='b', menustring='Back to start', node='node0'),
            ]),
            'node2' : MenuNode(text="Second node.  This node lists choices in two columns.", cmds=[
                CmdMenuCode(key='1', menustring='Set menutest attribute', code='self.caller.db.menutest="Testing!"; self.caller.msg("Attribute \'menutest\' set on you.  If you examine yourself, you can see it.")'),
                CmdMenuCode(key='2', menustring='Examine yourself', code='self.caller.msg("%s/%s = %s" % (self.caller.key, \'menutest\', self.caller.db.menutest))'),
                CmdMenuQuit(key='3', menustring='Quit'),
                CmdMenuCode(key='4', menustring='Remove attribute and quit', code='del self.caller.db.menutest; self.menutree.end(); self.caller.execute_cmd("look")'),
                # In practice for option '4', it's probably better to make your own Command class to do complex things like this, but this way works too.
            ]),
        })
        menu.goto('node0') # Start the menu

