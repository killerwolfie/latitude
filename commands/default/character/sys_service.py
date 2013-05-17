from ev import default_cmds

class CmdSysService(default_cmds.CmdService):
    """
    @service - manage services

    Usage:
      @service[/switch] <service>

    Switches:
      list   - shows all available services (default)
      start  - activates a service
      stop   - stops a service

    Service management system. Allows for the listing,
    starting, and stopping of services. If no switches
    are given, services will be listed.
    """

    key = "@service"
    aliases = ["@services"]
    locks = "cmd:pperm(command_@service) or pperm(Custodian)"
    help_category = "--- Coder/Sysadmin ---"

