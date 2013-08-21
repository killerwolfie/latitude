from game.gamesrc.latitude.commands.latitude_command import LatitudeCommand
from game.gamesrc.latitude.utils.archive import *
import pprint
import traceback
from ev import utils

class CmdSysAreaDump(LatitudeCommand):
    """
    @areadump - Output a data structure for the current area

    Usage:
      @areadump
        Outputs a data structure representing the current area, which can be read
        by the 'archive' utility classes.  This will typically only be of interest
        to coders who want to create instanced area generating routines, using
        some in-game template created by builders.
    """
    key = "@areadump"
    locks = "cmd:perm(command_@areadump) or perm(Janitors)"
    aliases = []
    help_category = "=== Admin ==="
    arg_regex = r"(/\w+?(\s|$))|\s|$"
    logged = True

    def func(self):
        hrule = "{x________________{W_______________{w_______________{W_______________{x_________________\n"
        area = self.character.get_area()
        exclude = self._all_protected(area)
        if area in exclude:
            exclude.remove(area)
        try:
            self.msg('%s\n{nArea : %s{n(%s)\n\n%s\n%s' % (hrule, area.get_desc_styled_name(looker=self.character), area.dbref, self._pformat(dump_objects([area], exclude=exclude)).replace('{', '{{').replace('%', '%%'), hrule))
        except UndumpableError:
            self.msg('{R----\nCould not dump this area.  This is most likely the result of an object with objects that point to unsupported object types.\n\n%s\n----' % (traceback.format_exc()))
        except:
            raise

    def _all_protected(self, obj):
        retval = []
        if utils.inherits_from(obj, 'game.gamesrc.latitude.objects.protected.Protected'):
            retval.append(obj)
        for con in obj.contents:
            retval.extend(self._all_protected(con))
        return retval

    def _pformat(self, obj, indent=0):
        retval = ''
        typ = type(obj)
        r = getattr(typ, "__repr__", None)
        if issubclass(typ, dict) and r is dict.__repr__:
            retval += '{\n'
            for key, ent in sorted(obj.items()):
                retval += ' ' * ((indent + 1) * 4) + repr(key) + ': ' + self._pformat(ent, indent + 1) + ',\n'
            retval += ' ' * (indent * 4) + '}'
        elif issubclass(typ, list) and r is list.__repr__:
            retval += '[\n'
            for ent in sorted(obj):
                retval += ' ' * ((indent + 1) * 4) + self._pformat(ent, indent + 1) + ',\n'
            retval += ' ' * (indent * 4) + ']'
        elif issubclass(typ, tuple) and r is tuple.__repr__:
            retval += '(\n'
            for ent in sorted(obj):
                retval += ' ' * ((indent + 1) * 4) + self._pformat(ent, indent + 1) + ',\n'
            retval += ' ' * (indent * 4) + ')'
        elif issubclass(typ, set) and r is set.__repr__:
            retval += 'set([\n'
            for ent in sorted(obj):
                retval += ' ' * ((indent + 1) * 4) + self._pformat(ent, indent + 1) + ',\n'
            retval += ' ' * (indent * 4) + '])'
        elif issubclass(typ, frozenset) and r is frozenset.__repr__:
            retval += 'frozenset([\n'
            for ent in sorted(obj):
                retval += ' ' * ((indent + 1) * 4) + self._pformat(ent, indent + 1) + ',\n'
            retval += ' ' * (indent * 4) + '])'
        else:
            retval = repr(obj)
        return retval
