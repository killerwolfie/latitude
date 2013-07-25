from ev import default_cmds

class CmdSysService(default_cmds.CmdService):
    """
    @service - Manage services

    Usage:
      @service/list
        Shows all available services

      @service/start <service>
        Activates a service

      @service/stop <service>
        Stops a service
    """

    key = "@service"
    aliases = ["@services"]
    locks = "cmd:perm(command_@service) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"
