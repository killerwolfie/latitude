from ev import Command
from ev import syscmdkeys
import random
from game.gamesrc.latitude.utils.evennia_color import *

class CmdNoMatch(Command):
    key = syscmdkeys.CMD_NOMATCH
    locks = "cmd:all()"
    auto_help = False

    def func(self):
        cmdline = self.args
        cmd = cmdline.split()[0]
        caller = self.caller
        sessid = self.sessid
        # Craft a message for the user
        if not hasattr(caller, 'player'):
            # Handle some commands which aren't available while OOC, but users are apt to try anyway, and give them special messages.
            lower_cmd = cmd[0].lower()
            if lower_cmd == 'look' or lower_cmd == 'l':
                self.cmd_ooc_look()
                return
            elif lower_cmd == 'say' or lower_cmd == 'pose' or cmdline.startswith(':') or cmdline.startswith('"'):
                self.msg("{R[You're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R]")
                return
        else:
            # If the character is IC, Check for a direction match, and tell them they can't go that way.
            for direction in [
                ('north', 'north'),
                ('south', 'south'),
                ('east', 'east'),
                ('west', 'west'),
                ('up', 'up'),
                ('down', 'down'),
                ('in', 'in'),
                ('out', 'out'),
                ('northeast', 'northeast'),
                ('northwest', 'northwest'),
                ('southeast', 'southeast'),
                ('southwest', 'southwest'),
                ('ne', 'northeast'),
                ('nw', 'northwest'),
                ('se', 'southeast'),
                ('sw', 'southwest'),
            ]:
                if direction[0].startswith(cmdline.lower()):
                    self.msg("You can't go %s right now." % direction[1])
                    return
        if cmd[0] == '@' or not hasattr(caller, 'player'):
            # Unknown command.
            self.msg('{R["%s" command not found.  (Try "{rhelp{R" for a list of commands)]' % cmd)
        else:
            # Unknown action.
            self.msg('You try to "%s" but it doesn\'t seem to work here.' % cmd)

    def cmd_ooc_look(self):
        player = self.caller
        # Display welcome screen
        self.msg('{w/-----------------------------------------------------------------------------\\')
        self.msg('{w| ' + evennia_color_left("{WWelcome, {w%s{W, to the world of {CLatitude MUD{W;" % player.get_desc_styled_name(self.caller), 75) + ' {w|')
        self.msg('{w| ' + evennia_color_right("{Wa massively multiplayer, online text adventure game.", 75) + ' {w|')
        self.msg('{w|                                                                             |')
        self.msg("{w|   {WTo join the game, use {w@char/ic <character name>{W to select a character.    {w|")
        self.msg('{w|                                                                             |')
        self.msg('{w|  {WSee {whelp{W for more information, or use {wpub <messsage>{W for the public chat.  {w|')
        self.msg('{w|-----------------------------------------------------------------------------|')
        disabled = player.no_slot_chars()
        characters = sorted(player.get_characters(), cmp=lambda b, a: cmp(a.db.stats_last_puppet_time, b.db.stats_last_puppet_time) or cmp(a.id, b.id))
        max_characters = player.max_characters()
        if max_characters != float('inf'):
            characters.extend([None] * (player.max_characters() - len(characters)))
        if characters:
            while characters:
                char_canvas = EvenniaColorCanvas()
                char_canvas.evennia_import('\n'.join(['{w|                                                                             |'] * 9))
                # Character #1
                if characters:
                    char_option = characters.pop(0)
                    if char_option:
                        char_canvas.draw_string(2, 1, self.character_block(char_option, disabled=char_option in disabled and 'No character slot'))
                    else:
                        char_canvas.draw_string(2, 1, self.empty_block())
                # Character #2
                if characters:
                    char_option = characters.pop(0)
                    if char_option:
                        char_canvas.draw_string(27, 1, self.character_block(char_option, disabled=char_option in disabled and 'No character slot'))
                    else:
                        char_canvas.draw_string(27, 1, self.empty_block())
                # Character #3
                if characters:
                    char_option = characters.pop(0)
                    if char_option:
                        char_canvas.draw_string(52, 1, self.character_block(char_option, disabled=char_option in disabled and 'No character slot'))
                    else:
                        char_canvas.draw_string(52, 1, self.empty_block())
                self.msg(char_canvas.evennia_export())
            self.msg('{w|                                                                             |')
        else:
            self.msg('{w|                                                                             |')
            self.msg('{w|' + evennia_color_center("{WNo characters yet.", 77) + '{w|')
            self.msg('{w|                                                                             |')
            self.msg('{w|' + evennia_color_center("{WUse {w@char/new <character name>{W to create one.", 77) + '{w|')
            self.msg('{w|' + evennia_color_center("{WSee {whelp @char{W for more information.", 77) + '{w|')
            self.msg('{w|                                                                             |')
        self.msg('{w|-----------------------------------------------------------------------------|')
        self.msg('{w|' + evennia_color_center('{WIf you have any questions or comments, email {wstaff@latitude.muck.ca{W.', 77) + '{w|')
        self.msg('{w\\-----------------------------------------------------------------------------/')
        return

    def character_block(self, character, disabled=False):
        """
        Create a 24x8 info square for a character
        """
        block_canvas = EvenniaColorCanvas()
        block_canvas.evennia_import((disabled and '{R' or '{W') + self.character_border())
        block_canvas.draw_string(1, 1, evennia_color_center(character.get_desc_styled_name(self.caller), 22, dots=True))
        block_canvas.draw_string(1, 3, evennia_color_left('{nSex: %s{n' % (character.get_desc_styled_gender(self.caller)), 12, dots=True))
        block_canvas.draw_string(14, 3, evennia_color_left('{nSta: {g%s{n' % (character.game_attribute('STAMINA')), 9, dots=True))
        if disabled:
            block_canvas.draw_string(1, 6, evennia_color_center('{r' + disabled, 22, dots=True))
        return block_canvas.evennia_export()

    def empty_block(self):
        """
        Create a 24x8 info square, but for an empty slot with no character
        """
        block_canvas = EvenniaColorCanvas()
        block_canvas.evennia_import('{W' + self.character_border())
        block_canvas.draw_string(1, 3, evennia_color_center('{wEMPTY SLOT', 22, dots=True))
        block_canvas.draw_string(1, 4, evennia_color_center('{W{w@char/new{W to create', 22, dots=True))
        return block_canvas.evennia_export()
        

    def character_border(self):
        return (
            '/' + '-' * 22 + '\\\n' +
            ('|' + ' ' * 22 + '|\n') * 6 +
            '\\' + '-' * 22 + '/'
        )

