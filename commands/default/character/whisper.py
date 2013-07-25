from ev import default_cmds
import random
import re

class CmdWhisper(default_cmds.MuxPlayerCommand):
    """
    whisper - speak quietly

    Usage:
      whisper <text>
        Speak softly to nobody in particular.  The other people in the room may or
        may not hear you.

      whisper <text> to <object> (or whisper <object>=<text>)
        Whisper a message to a specific object (which could be a character) in the
        room.  Only that character or object will hear your message.
    """

    key = "whisper"
    aliases = ['w ']
    locks = "cmd:all()"
    help_category = "Actions"
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.character
        # Parse command line
        if self.lhs and self.rhs:
            target = character.search(self.lhs)
            raw_message = self.rhs
            if not target:
                return # Search should have output a message
        else:
            match = re.search(r'^(.*)\s+to\s+(\S*)$', self.args)
            if match:
                target = character.search(match.group(2))
                raw_message = match.group(1)
            else:
                target = None
                raw_message = self.args
        # Sanity check
        if target == character:
            self.msg('They say talking to yourself is a sign of genius.')
            return
        if target == character.location:
            target = None
        # Fancy up the message
        message = self.character.speech_msg(raw_message, min_depth=1)
        # Deliver the message
        if target:
            self.msg(character.objsub('{nYou whisper "%s{n" to &1c.' % (message), target))
            target.msg(character.objsub('{n&0N whispers "%s{n" to you.' % (message), target))
            target.at_whisper(character, raw_message)
        else:
            self.msg('{nYou whisper "%s{n".' % (message))
            if character.location:
                for con in character.location.contents:
                    if con == character:
                        continue
                    if random.random() < 0.4:
                        con.msg(character.objsub('{n&0N whispers "%s{n".' % (message), target))
                    else:
                        con.msg(character.objsub('{n&0N whispers something.', target))
                character.location.at_whisper(character, raw_message)
