from src.commands.default.muxcommand import MuxCommand

class CmdUnconnectedHelp(MuxCommand):
    """
    This is an unconnected version of the help command,
    for simplicity. It shows a pane of info.
    """
    key = "help"
    aliases = ["h", "?"]
    locks = "cmd:all()"

    def func(self):
        "Shows help"

        string = \
            """
You are not yet logged into the game. Commands available at this point:
  {wcreate, connect, look, help, quit{n

To login to the system, you need to do one of the following:

{w1){n If you have no previous account, you need to use the 'create'
   command.

     {wcreate Anna c67jHL8p{n

   Note that if you use spaces in your name, you have to enclose in quotes.

     {wcreate "Anna the Barbarian"  c67jHL8p{n

   It's always a good idea (not only here, but everywhere on the net)
   to not use a regular word for your password. Make it longer than
   6 characters or write a passphrase.

{w2){n If you have an account already, either because you just created
   one in {w1){n above or you are returning, use the 'connect' command:

     {wconnect Anna c67jHL8p{n

   (Again, if there are spaces in the name you have to enclose it in quotes).
   This should log you in. Run {whelp{n again once you're logged in
   to get more aid. Hope you enjoy your stay!

You can use the {wlook{n command if you want to see the connect screen again.
"""
        self.caller.msg(string)
