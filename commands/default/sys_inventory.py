from ev import default_cmds

class CmdSysInventory(default_cmds.CmdInventory):
    """
    inventory

    Usage:
      inventory
      inv

    Shows your inventory.
    """
    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"

