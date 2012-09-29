#from src.utils import utils
#from src.commands.connection_screen import DEFAULT_SCREEN

CUSTOM_SCREEN = \
"""%cn%cc _____________________________________________________________________________
%cc /~~\_______/~~~~~~\__/~~~~~~\_/~~~\_/~~~~~~\_/~~\__/~~\_/~~~~~~~\__/~~~~~~~~\\
%cc /~~\______/~~\__/~~\___/~~\____/~\____/~~\___/~~\__/~~\_/~~\__/~~\_/~~\______
%cc /~~\______/~~~~~~~~\___/~~\____/~\____/~~\___/~~\__/~~\_/~~\__/~~\_/~~~~~~\__
%cc /~~\______/~~\__/~~\___/~~\____/~\____/~~\___/~~\__/~~\_/~~\__/~~\_/~~\______
%cc /~~~~~~~\_/~~\__/~~\___/~~\___/~~~\___/~~\____/~~~~~~\__/~~~~~~~\__/~~~~~~~~\\
%cc _____________________________________________________________________________
%cc ___________________/\/\______/\/\___/\/\____/\/\____/\/\/\/\/\_______________
%cc ___%chWelcome to%cn%cc_____/\/\/\__/\/\/\___/\/\____/\/\____/\/\____/\/\______________
%cc ____%chLatitude%cn%cc_____/\/\/\/\/\/\/\___/\/\____/\/\____/\/\____/\/\_______________
%cc ______%chMUD!%cn%cc______/\/\__/\__/\/\___/\/\____/\/\____/\/\____/\/\________________
%cc _______________/\/\______/\/\_____/\/\/\/\______/\/\/\/\/\___________________
%cc _____________________________________________________________________________
%cn
 You're connected to Lat.  A multi-user virtual world.
             "Latitude n. Room; space; freedom from confinement or restraint."
                                                           latitude.muck.ca
                                                        Port: 23 SSL Port: 992

      To connect to your character use 'connect <playername> <password>'
          New here? To connect as a guest, use 'connect guest guest'
        Or, To create a character use 'create <playername> <password>'

{n"""

# # Mux-like alternative screen for contrib/mux_login.py

# MUX_SCREEN = \
# """{b=============================================================={n
# Welcome to {gEvennia{n, version %s!
#
# If you have an existing account, connect to it by typing:
#      {wconnect <email> <password>{n
# If you need to create an account, type (without the <>'s):
#      {wcreate \"<username>\" <email> <password>{n
#
# Enter {whelp{n for more info. {wlook{n will re-load this screen.
#{b=============================================================={n""" % utils.get_evennia_version()

# # Menu login minimal header for contrib/menu_login.py

# MENU_SCREEN = \
# """{b=============================================================={n
#  Welcome to {gEvennnia{n, version %s!
# {b=============================================================={n""" % utils.get_evennia_version()
