from ev import default_cmds
from ev import utils
from src.commands import cmdhandler
from src.objects.models import ObjAttribute
from src.players.models import PlayerAttribute
from src.utils.ansi import raw

class CmdSysExamine(default_cmds.ObjManipCommand):
    """
    examine - detailed info on objects

    Usage:
      examine [<object>[/attrname]]
      examine [*<player>[/attrname]]

    Switch:
      player - examine a Player (same as adding *)

    The examine command shows detailed game info about an
    object and optionally a specific attribute on it.
    If object is not specified, the current location is examined.

    Append a * before the search string to examine a player.

    """
    key = "@examine"
    aliases = []
    locks = "cmd:pperm(command_sys_examine) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    player_mode = False

    def list_attribute(self, crop, attr, value):
        """
        Formats a single attribute line.
        """
        if crop and isinstance(value, basestring):
            value = utils.crop(value)
            value = utils.to_unicode(value)
        string = "\n %s = %s" % (attr, value)
        string = raw(string)
        return string

    def format_attributes(self, obj, attrname=None, crop=True):
        """
        Helper function that returns info about attributes and/or
        non-persistent data stored on object
        """

        if attrname:
            db_attr = [(attrname, obj.attr(attrname))]
            try:
                ndb_attr = [(attrname, object.__getattribute__(obj.ndb, attrname))]
            except Exception:
                ndb_attr = None
        else:
            if self.player_mode:
                db_attr = [(attr.key, attr.value) for attr in PlayerAttribute.objects.filter(db_obj=obj)]
            else:
                db_attr = [(attr.key, attr.value) for attr in ObjAttribute.objects.filter(db_obj=obj)]
            try:
                ndb_attr = [(aname, avalue) for aname, avalue in obj.ndb.__dict__.items() if not aname.startswith("_")]
            except Exception:
                ndb_attr = None
        string = ""
        if db_attr and db_attr[0]:
            string += "\n{wPersistent attributes{n:"
            for attr, value in db_attr:
                string += self.list_attribute(crop, attr, value)
        if ndb_attr and ndb_attr[0]:
            string += "\n{wNon-Persistent attributes{n:"
            for attr, value in ndb_attr:
                string += self.list_attribute(crop, attr, value)
        return string

    def format_output(self, obj, avail_cmdset):
        """
        Helper function that creates a nice report about an object.

        returns a string.
        """

        string = "\n{wName/key{n: {c%s{n (%s)" % (obj.name, obj.dbref)
        if hasattr(obj, "aliases") and obj.aliases:
            string += "\n{wAliases{n: %s" % (", ".join(utils.make_iter(obj.aliases)))
        if hasattr(obj, "sessid") and obj.sessid:
            string += "\n{wsession{n: %s" % obj.sessid
        elif hasattr(obj, "sessions") and obj.sessions:
            string += "\n{wsession(s){n: %s" % (", ".join(str(sess.sessid) for sess in obj.sessions))
        if hasattr(obj, "has_player") and obj.has_player:
            string += "\n{wPlayer{n: {c%s{n" % obj.player.name
            perms = obj.player.permissions
            if obj.player.is_superuser:
                perms = ["<Superuser>"]
            elif not perms:
                perms = ["<None>"]
            string += "\n{wPlayer Perms{n: %s" % (", ".join(perms))
        string += "\n{wTypeclass{n: %s (%s)" % (obj.typeclass.typename, obj.typeclass_path)
        if hasattr(obj, "location"):
            string += "\n{wLocation{n: %s" % obj.location
            if obj.location:
                string += " (#%s)" % obj.location.id
        if hasattr(obj, "destination"):
            string += "\n{wDestination{n: %s" % obj.destination
            if obj.destination:
                string += " (#%s)" % obj.destination.id
        perms = obj.permissions
        if perms:
            perms_string = (", ".join(perms))
        else:
            perms_string = "Default"
        if obj.is_superuser:
            perms_string += " [Superuser]"

        string += "\n{wPermissions{n: %s" % perms_string
        locks = str(obj.locks)
        if locks:
            locks_string = utils.fill("; ".join([lock for lock in locks.split(';')]), indent=6)
        else:
            locks_string = " Default"


        string += "\n{wLocks{n:%s" % locks_string

        if not (len(obj.cmdset.all()) == 1 and obj.cmdset.current.key == "Empty"):
            # list the current cmdsets
            all_cmdsets = obj.cmdset.all() + (hasattr(obj, "player") and obj.player and obj.player.cmdset.all() or [])
            all_cmdsets.sort(key=lambda x:x.priority, reverse=True)
            string += "\n{wCurrent Cmdset(s){n:\n %s" % ("\n ".join("%s (prio %s)" % (cmdset.path, cmdset.priority) for cmdset in all_cmdsets))

            # list the commands available to this object
            avail_cmdset = sorted([cmd.key for cmd in avail_cmdset if cmd.access(obj, "cmd")])

            cmdsetstr = utils.fill(", ".join(avail_cmdset), indent=2)
            string += "\n{wCommands available to %s (all cmdsets + exits and external cmds){n:\n %s" % (obj.key, cmdsetstr)

        if hasattr(obj, "scripts") and hasattr(obj.scripts, "all") and obj.scripts.all():
            string += "\n{wScripts{n:\n %s" % obj.scripts
        # add the attributes
        string += self.format_attributes(obj)
        # add the contents
        exits = []
        pobjs = []
        things = []
        if hasattr(obj, "contents"):
            for content in obj.contents:
                if content.destination:
                    exits.append(content)
                elif content.player:
                    pobjs.append(content)
                else:
                    things.append(content)
            if exits:
                string += "\n{wExits{n: %s" % ", ".join([exit.name for exit in exits])
            if pobjs:
                string += "\n{wCharacters{n: %s" % ", ".join(["{c%s{n" % pobj.name for pobj in pobjs])
            if things:
                string += "\n{wContents{n: %s" % ", ".join([cont.name for cont in obj.contents
                                                           if cont not in exits and cont not in pobjs])
        separator = "-"*78
        #output info
        return '%s\n%s\n%s' % ( separator, string.strip(), separator )

    def func(self):
        "Process command"
        caller = self.caller

        def get_cmdset_callback(cmdset):
            """
            We make use of the cmdhandeler.get_and_merge_cmdsets below. This
            is an asynchronous function, returning a Twisted deferred.
            So in order to properly use this we need use this callback;
            it is called with the result of get_and_merge_cmdsets, whenever
            that function finishes. Taking the resulting cmdset, we continue
            to format and output the result.
            """
            string = self.format_output(obj, cmdset)
            self.msg(string.strip())

        if not self.args:
            # If no arguments are provided, examine the invoker's location.
            if hasattr(caller, "location"):
                obj = caller.location
                # using callback for printing result whenever function returns.
                cmdhandler.get_and_merge_cmdsets(obj).addCallback(get_cmdset_callback)
            else:
                self.msg("You need to supply a target to examine.")
            return

        # we have given a specific target object
        for objdef in self.lhs_objattr:

            obj_name = objdef['name']
            obj_attrs = objdef['attrs']

            self.player_mode = utils.inherits_from(caller, "src.players.player.Player") or \
                                "player" in self.switches or obj_name.startswith('*')
            if self.player_mode:
                try:
                    obj = caller.search_player(obj_name.lstrip('*'))
                except AttributeError:
                    # this means we are calling examine from a player object
                    obj = caller.search(obj_name.lstrip('*'))
            else:
                obj = caller.search(obj_name)
            if not obj:
                continue

            if obj_attrs:
                for attrname in obj_attrs:
                    # we are only interested in specific attributes
                    caller.msg(self.format_attributes(obj, attrname, crop=False))
            else:
                # using callback to print results whenever function returns.
                cmdhandler.get_and_merge_cmdsets(obj).addCallback(get_cmdset_callback)

