from ev import default_cmds

class CmdPose(default_cmds.CmdPose):
    """
    pose - strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """
    key = "pose"
    aliases = [":", "emote"]
    locks = "cmd:all()"
