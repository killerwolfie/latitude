import re
import traceback

from src.commands.default.muxcommand import MuxCommand

class CmdUnconnectedQuit(MuxCommand):
    """
    We maintain a different version of the quit command
    here for unconnected players for the sake of simplicity. The logged in
    version is a bit more complicated.
    """
    key = "quit"
    aliases = ["q", "qu"]
    locks = "cmd:all()"

    def func(self):
        "Simply close the connection."
        session = self.caller
        session.msg("Good bye! Disconnecting ...")
        session.session_disconnect()

