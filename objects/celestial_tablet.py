from game.gamesrc.latitude.objects.item import Item
from game.gamesrc.latitude.utils.editobj import EditObj
from ev import utils

class CelestialTablet(Item):
    """
    This item is used by builders to edit and create objects.
    """
    def basetype_setup(self):
        """
        This sets up the default properties of an Object,
        just before the more general at_object_creation.
        """
        super(CelestialTablet, self).basetype_setup()
        self.locks.add(";".join([
            "get:false()",                # For security reasons keep these things from being picked up
            "drop:false()",               # For security reasons keep these things from dropping
        ]))

    def action_use(self, user):
        user.msg('STUB: Celestial tablet use')

    def action_use_on(self, user, targets):
        if len(targets) != 1:
            user.msg('You can only use that on one one thing at a time.')
            return
        target = targets[0]
        # Check the default permission type
        area = target.get_area()
        if not (area.access(user, 'area_build')):
            return # The access check should spew a message if needed
        # Generate the EditObj fields
        editobj_fields = [
            {
                'key'  : '1',
                'type' : 'NAME',
                'menutext' : '{C[{c1{C] Name:   ',
                'desc' : 'Name',
                'cols' : 2,
            },
            {
                'type' : 'SEP',
                'menutext' : 'Descriptions',
                'cols' : 1,
            },
            {
                'key' : 'D1',
                'type' : 'ATTR',
                'menutext' : '{C[{cD1{C] Appearance: ',
                'desc' : 'Appearance',
                'attribute' : 'desc_appearance',
                'cols' : 1,
                'color' : True,
            },
            {
                'key' : 'D2',
                'type' : 'ATTR',
                'menutext' : '{C[{cD2{C] Scent:      ',
                'desc' : 'Scent',
                'attribute' : 'desc_scent',
                'cols' : 1,
                'color' : True,
            },
            {
                'key' : 'D3',
                'type' : 'ATTR',
                'menutext' : '{C[{cD3{C] Texture:    ',
                'desc' : 'Texture',
                'attribute' : 'desc_texture',
                'cols' : 1,
                'color' : True,
            },
            {
                'key' : 'D4',
                'type' : 'ATTR',
                'menutext' : '{C[{cD4{C] Flavor:     ',
                'desc' : 'Flavor',
                'attribute' : 'desc_flavor',
                'cols' : 1,
                'color' : True,
            },
            {
                'key' : 'D5',
                'type' : 'ATTR',
                'menutext' : '{C[{cD5{C] Aura:       ',
                'desc' : 'Aura',
                'attribute' : 'desc_aura',
                'cols' : 1,
                'color' : True,
            },
            {
                'key' : 'D6',
                'type' : 'ATTR',
                'menutext' : '{C[{cD6{C] Sound:      ',
                'desc' : 'Sound',
                'attribute' : 'desc_sound',
                'cols' : 1,
                'color' : True,
            },
            {
                'key' : 'D7',
                'type' : 'ATTR',
                'menutext' : '{C[{cD7{C] Writing:    ',
                'desc' : 'Writing',
                'attribute' : 'desc_writing',
                'cols' : 1,
                'color' : True,
            },
        ]
        if utils.inherits_from(target, 'game.gamesrc.latitude.objects.item.Item'):
            pass
        if utils.inherits_from(target, 'game.gamesrc.latitude.objects.room.Room'):
            pass
        else:
            user.msg("{R[This item can't modify that object type]")
            return
        # Start the edit
        editobj = EditObj(caller=user, obj=target, key=self.key, sessid=user.sessid, fields=editobj_fields)
        editobj.editkit = self
