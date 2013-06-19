from ev import default_cmds
from src.utils import prettytable
from src.scripts.models import ScriptDB

class CmdSysScripts(default_cmds.CmdScripts):
    """
    Operate and list global scripts, list all scrips.

    Usage:
      @scripts[/switches] [<obj or scriptid or script.path>]

    Switches:
      start - start a script (must supply a script path)
      stop - stops an existing script
      kill - kills a script - without running its cleanup hooks
      validate - run a validation on the script(s)

    If no switches are given, this command just views all active
    scripts. The argument can be either an object, at which point it
    will be searched for all scripts defined on it, or an script name
    or dbref. For using the /stop switch, a unique script dbref is
    required since whole classes of scripts often have the same name.

    Use @script for managing commands on objects.
    """
    key = "@scripts"
    aliases = []
    locks = "cmd:perm(command_@scripts) or perm(Janitors)"
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"

    def func(self):
        "implement method"

        caller = self.caller
        args = self.args

        string = ""
        if args:
            if "start" in self.switches:
                # global script-start mode
                new_script = create.create_script(args)
                if new_script:
                    caller.msg("Global script %s was started successfully." % args)
                else:
                    caller.msg("Global script %s could not start correctly. See logs." % args)
                return

            # test first if this is a script match
            scripts = ScriptDB.objects.get_all_scripts(key=args)
            if not scripts:
                # try to find an object instead.
                objects = ObjectDB.objects.object_search(args, caller=caller)
                if objects:
                    scripts = []
                    for obj in objects:
                        # get all scripts on the object(s)
                        scripts.extend(ScriptDB.objects.get_all_scripts_on_obj(obj))
        else:
            # we want all scripts.
            scripts = ScriptDB.objects.get_all_scripts()
            if not scripts:
                caller.msg("No scripts are running.")
                return

        if not scripts:
            string = "No scripts found with a key '%s', or on an object named '%s'." % (args, args)
            caller.msg(string)
            return

        if self.switches and self.switches[0] in ('stop', 'del', 'delete', 'kill'):
            # we want to delete something
            if not scripts:
                string = "No scripts/objects matching '%s'. " % args
                string += "Be more specific."
            elif len(scripts) == 1:
                # we have a unique match!
                if 'kill' in self.switches:
                    string = "Killing script '%s'" % scripts[0].key
                    scripts[0].stop(kill=True)
                else:
                    string = "Stopping script '%s'." % scripts[0].key
                    scripts[0].stop()
                #import pdb
                #pdb.set_trace()
                ScriptDB.objects.validate() #just to be sure all is synced
            else:
                # multiple matches.
                string = "Multiple script matches. Please refine your search:\n"
                string += format_script_list(scripts)
        elif self.switches and self.switches[0] in ("validate", "valid", "val"):
            # run validation on all found scripts
            nr_started, nr_stopped = ScriptDB.objects.validate(scripts=scripts)
            string = "Validated %s scripts. " % ScriptDB.objects.all().count()
            string += "Started %s and stopped %s scripts." % (nr_started, nr_stopped)
        else:
            # No stopping or validation. We just want to view things.
            string = format_script_list(scripts)
        caller.msg(string)

def format_script_list(scripts):
    "Takes a list of scripts and formats the output."
    if not scripts:
        return "<No scripts>"

    table = prettytable.PrettyTable(["{wid","{wobj","{wkey","{wintval","{wnext","{wrept","{wdb"," {wtypeclass","{wdesc"],align='r')
    table.align = 'r'
    for script in scripts:
        nextrep = script.time_until_next_repeat()
        table.add_row([script.id,
                       (not hasattr(script, 'obj') or not script.obj) and "<Global>" or script.obj.key,
                       script.key,
                       (not hasattr(script, 'interval') or script.interval < 0) and "--" or "%ss" % script.interval,
                       not nextrep and "--" or "%ss" % nextrep,
                       (not hasattr(script, 'repeats') or not script.repeats) and "--" or "%i" % script.repeats,
                       script.persistent and "*" or "-",
                       script.typeclass_path.rsplit('.', 1)[-1],
                       hasattr(script, 'desc_script') and script.desc_script() or script.desc])
    return "%s" % table
