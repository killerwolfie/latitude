from ev import default_cmds

class CmdSysOOC(default_cmds.CmdOOC):
    """
    go ooc

    Usage:
      @ooc

    Go out-of-character (OOC).

    This will leave your current character, and bring you to the 'OOC' account menu.
    """

    key = "@ooc"
    locks = "cmd:all()" # this must be all(), or different puppeted objects won't be able to access it.
    aliases = "@unpuppet"
    help_category = "General"

    def func(self):
        "Implement function"

        player = self.caller
        sessid = self.sessid

        old_char = player.get_puppet(sessid)
        if not old_char:
            string = "You are already OOC."
            self.msg(string)
            return

        player.db._last_puppet = old_char
        if old_char.location:
            old_char.location.msg_contents("%s has left the game." % old_char.key, exclude=[old_char])

        # disconnect
        if player.unpuppet_object(sessid):
            self.msg("\n{GYou go OOC.{n\n")
            player.execute_cmd("look", sessid=sessid)
        else:
            raise RuntimeError("Could not unpuppet!")

