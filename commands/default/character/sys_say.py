from ev import default_cmds

class CmdSysSay(default_cmds.MuxPlayerCommand):
    """
    @say
    
    Speak or pose with an Out of Character marker. Use this to make sure people
    can tell you're not roleplaying.

    Also, this is not an in-game action, so it doesn't trigger any 'say' sensitive
    events.

    Usage:
        @say <text>
        @say :<pose>

    Example:
      @say Hello, there!
       -> others will see:
      [OOC] Tom says, "Hello, there!"

    Example 2:
      @say :waves.
       -> others will see:
      [OOC] Tom waves.
    """
    key = "@say"
    locks = "cmd:all()"
    help_category = "Communication"
    aliases = ['ooc']
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.character
        if self.args.startswith(':'):
            message = character.speech_pose(self.args[1:])
        elif self.args.startswith('"'):
            message = character.speech_say(self.args[1:])
        else:
            message = character.speech_say(self.args)
        message = '{Y[ {rOOC {Y| {n%s {Y]' % message
        if character.location:
            character.location.msg_contents(message)
        else:
            character.msg(message)
