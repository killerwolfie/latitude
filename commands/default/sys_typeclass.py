from ev import default_cmds

class CmdSysTypeclass(default_cmds.CmdTypeclass):
    """
    @typeclass - set object typeclass

    Usage:
      @typclass[/switch] <object> [= <typeclass.path>]
      @type                     ''
      @parent                   ''

    Switch:
      reset - clean out *all* the attributes on the object -
              basically making this a new clean object.
      force - change to the typeclass also if the object
              already has a typeclass of the same name.
    Example:
      @type button = examples.red_button.RedButton

    View or set an object's typeclass. If setting, the creation hooks
    of the new typeclass will be run on the object. If you have
    clashing properties on the old class, use /reset. By default you
    are protected from changing to a typeclass of the same name as the
    one you already have, use /force to override this protection.

    The given typeclass must be identified by its location using
    python dot-notation pointing to the correct module and class. If
    no typeclass is given (or a wrong typeclass is given). Errors in
    the path or new typeclass will lead to the old typeclass being
    kept. The location of the typeclass module is searched from the
    default typeclass directory, as defined in the server settings.

    """

    key = "@typeclass"
    aliases = "@type, @parent"
    locks = "cmd:perm(typeclass) or perm(Builders)"
    help_category = "Building"

