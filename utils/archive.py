from ev import create_object, search_object
from collections import defaultdict, MutableSequence, MutableSet, MutableMapping

class UndumpableError(Exception):
    pass

def dump_objects(objects, with_children=True):
    if with_children:
        all_children = []
        for obj in objects:
            all_children.extend(_get_all_children(obj))
        objects = all_children
    objspec = {}
    for obj in objects:
        obj = obj.typeclass
        spec = {}
        # TODO: Nicks.  Doesn't seem to have a way to grab them all as a hash
        # TODO: Scripts?  These might be better off not something that gets archived.
        # Store data
        spec['typeclass'] = str(obj.path)
        spec['key'] = unicode(obj.key)
        spec['aliases'] = list(obj.aliases)
        spec['permissions'] = list(obj.permissions)
        spec['locks'] = str(obj.locks)
        if not obj.location:
            spec['location'] = None
        elif obj.location in objects:
            spec['location'] = 'obj_%d' % obj.location.id
        else:
            spec['location'] = obj.location.dbref
        if not obj.home:
            spec['home'] = None
        elif obj.home in objects:
            spec['home'] = 'obj_%d' % obj.home.id
        else:
            spec['home'] = obj.home.dbref
        if not obj.destination:
            spec['destination'] = None
        elif obj.destination in objects:
            spec['destination'] = 'obj_%d' % obj.destination.id
        else:
            spec['destination'] = obj.destination.dbref
        # Store db attributes
        spec['db'] = {}
        for attr in obj.get_all_attributes():
            spec['db'][attr.key] = _clean_attribute(attr.value)
        # Save the spec for return
        objspec['obj_%d' % obj.id] = spec
    return objspec

def _get_all_children(obj):
    retval = [obj]
    for con in obj.contents:
        retval.extend(_get_all_children(con))
    return retval

def _clean_attribute(attrval):
    if isinstance(attrval, MutableSequence):
        return [_clean_attribute(val) for val in attrval]
    elif isinstance(attrval, MutableSet):
        return set(_clean_attribute(val) for val in attrval)
    elif isinstance(attrval, MutableMapping):
        return dict((_clean_attribute(key), _clean_attribute(val)) for key, val in attrval)
    elif isinstance(attrval, (basestring, int, float, long, complex)):
        return attrval
    else:
        raise UndumpableError('object type not supported: %r' % attrval)

def load_objects(objspec):
    objects = {}
    # Create objects
    for identifier, spec in objspec.iteritems():
        obj = create_object(spec['typeclass'])
        if 'key' in spec:
            obj.key = spec['key']
        if 'aliases' in spec:
            obj.aliases = spec['aliases']
        if 'permissions' in spec:
            obj.permissions = spec['permissions']
        if 'locks' in spec:
            obj.locks.replace(spec['locks'])
        if 'db' in spec:
            for key, val in spec['db'].iteritems():
                obj.set_attribute(key, val)
        objects[identifier] = obj
    # Handle links between objects
    for identifier, spec in objspec.iteritems():
        if 'location' in spec:
            if spec['location'].startswith('#'):
                objects[identifier].location = search_object(spec['location'])[0]
            else:
                objects[identifier].location = objects[spec['location']]
        if 'home' in spec:
            if spec['home'].startswith('#'):
                objects[identifier].home = ev.search_object(spec['home'])[0]
            else:
                objects[identifier].home = objects[spec['home']]
        if 'destination' in spec:
            if spec['destination'].startswith('#'):
                objects[identifier].destination = ev.search_object(spec['destination'])[0]
            else:
                objects[identifier].destination = objects[spec['destination']]
    return objects
