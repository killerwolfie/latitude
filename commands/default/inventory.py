from ev import default_cmds

class CmdInventory(default_cmds.CmdInventory):
    """
    inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv"]
    locks = "cmd:all()"
    help_category = 'Actions'
