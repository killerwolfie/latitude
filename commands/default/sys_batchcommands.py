from ev import default_cmds

class CmdSysBatchCommands(default_cmds.CmdBatchCommands):
    """
    Build from batch-command file

    Usage:
     @batchcommands[/interactive] <python.path.to.file>

    Switch:
       interactive - this mode will offer more control when
                     executing the batch file, like stepping,
                     skipping, reloading etc.

    Runs batches of commands from a batch-cmd text file (*.ev).

    """
    key = "@batchcommands"
    locks = "cmd:pperm(batchcommands) or superuser()"
    help_category = "--- Coder/Sysadmin ---"

