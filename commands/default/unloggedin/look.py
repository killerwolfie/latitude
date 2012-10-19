"""
Commands that are available from the connect screen.
"""
import re
import traceback
from django.conf import settings

from src.utils import utils, ansi
from src.commands.default.muxcommand import MuxCommand
from src.commands.cmdhandler import CMD_LOGINSTART

# limit symbol import for API
__all__ = ("CmdUnconnectedConnect", "CmdUnconnectedCreate", "CmdUnconnectedQuit", "CmdUnconnectedLook", "CmdUnconnectedHelp")

CONNECTION_SCREEN_MODULE = settings.CONNECTION_SCREEN_MODULE
CONNECTION_SCREEN = ""
try:
    CONNECTION_SCREEN = ansi.parse_ansi(utils.string_from_module(CONNECTION_SCREEN_MODULE))
except Exception:
    pass
if not CONNECTION_SCREEN:
    CONNECTION_SCREEN = "\nEvennia: Error in CONNECTION_SCREEN MODULE (randomly picked connection screen variable is not a string). \nEnter 'help' for aid."

class CmdUnconnectedLook(MuxCommand):
    """
    This is an unconnected version of the look command for simplicity.

    This is called by the server and kicks everything in gear.
    All it does is display the connect screen.
    """
    key = CMD_LOGINSTART
    aliases = ["look", "l"]
    locks = "cmd:all()"

    def func(self):
        "Show the connect screen."
        self.caller.msg(CONNECTION_SCREEN)
