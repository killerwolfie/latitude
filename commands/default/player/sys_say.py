from game.gamesrc.latitude.commands.default.character import say

class CmdSysSay(say.CmdSay):
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
      <OOC> Tom says, "Hello, there!"

    Example 2:
      @say :waves.
       -> others will see:
      <OOC> Tom waves.
    """
    key = "@say"
    locks = "cmd:all()"
    help_category = "Communication"
    aliases = ['ooc']
    arg_regex = r"\s.*?|$"

    def func(self):
        character = self.character
        if character:
            if self.args.startswith(':'):
                message = self.gen_pose(self.args[1:])
            elif self.args.startswith('"'):
                message = self.gen_say(self.args[1:])
            else:
                message = self.gen_say(self.args)
            message = '{w<{rOOC{w> {n' + message
            if self.character.location:
                self.character.location.msg_contents(message)
            else:
                self.character.msg(message)
        else:
            self.msg("{RYou're not currently playing any character.  See {rhelp @char{R for help, or try talking on the public channel with {rpub <message>{R.")
