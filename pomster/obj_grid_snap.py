# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from mathutils import Vector
import bpy

GRID_SIZE_CPROP_NAME = "poms_grid_size"
DEFAULT_TARGET_OBJ_NAME = "GridSnapTarget"

DIM_XYZ = ("X", "Y", "Z")
def add_object_grid_snap_drivers(ob, target_ob):
    ob[GRID_SIZE_CPROP_NAME] = Vector((1, 1, 1))

    drv_data_item = ob
    for d in range(len(DIM_XYZ)):
        dim_str = DIM_XYZ[d]
        new_drv = drv_data_item.driver_add("location", d).driver
        new_drv.type = "SCRIPTED"
        new_var = new_drv.variables.new()
        new_var.name = "location"
        new_var.type = "SINGLE_PROP"
        new_var.targets[0].id_type = "OBJECT"
        new_var.targets[0].id = target_ob
        new_var.targets[0].transform_space = "WORLD_SPACE"
        new_var.targets[0].transform_type = "LOC_" + dim_str
        new_var.targets[0].rotation_mode = "AUTO"
        new_var.targets[0].data_path = "location[" + str(d) + "]"
        new_var = new_drv.variables.new()
        new_var.name = "grid_size"
        new_var.type = "SINGLE_PROP"
        new_var.targets[0].id_type = "OBJECT"
        new_var.targets[0].id = ob
        new_var.targets[0].transform_space = "WORLD_SPACE"
        new_var.targets[0].transform_type = "LOC_" + dim_str
        new_var.targets[0].rotation_mode = "AUTO"
        new_var.targets[0].data_path = "[\""+GRID_SIZE_CPROP_NAME+"\"][" + str(d) + "]"
        new_drv.expression = "floor(location / grid_size) * grid_size"

def set_active_object(ob):
    bpy.context.view_layer.objects.active = ob

def add_object_grid_snap(context, act_ob, sel_ob):
    # if no other object (target object) selected then create an empty to use as default target object
    if len(sel_ob) < 1:
        bpy.ops.object.empty_add(type='ARROWS', location=act_ob.location)
        new_thing = context.active_object
        new_thing.name = DEFAULT_TARGET_OBJ_NAME
        target_ob = new_thing
    else:
        target_ob = sel_ob[0]

    add_object_grid_snap_drivers(act_ob, target_ob)

    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # select objects that were originally selected
    act_ob.select_set(True)
    target_ob.select_set(True)
    set_active_object(act_ob)

class POMSTER_AddObjGridSnap(bpy.types.Operator):
    bl_description = "Add drivers to snap active object's location to grid. If two objects selected (active and " \
        "Target) then Target object's location is input to active object's Grid Snap. If one object selected then " \
        "Empty is created for Target"
    bl_idname = "pomster.add_object_grid_snap"
    bl_label = "Object Grid Snap"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        act_ob = context.active_object
        if len(context.selected_objects) > 2:
            self.report({'ERROR'}, "Too many objects selected, cannot Add Object Grid Snap. Select 1 or 2 objects " +
                        "and try again.")
            return {'CANCELLED'}
        if act_ob is None or act_ob not in context.selected_objects:
            self.report({'ERROR'}, "No object is active or active object is not selected, so cannot Add Object Grid " +
                        "Snap. Select 1 or 2 objects and try again.")
            return {'CANCELLED'}
        # get selected object that is in selected_objects collection if is not the active_object
        sel_ob = [ ob for ob in bpy.context.selected_objects if ob != act_ob ]
        add_object_grid_snap(context, act_ob, sel_ob)
        return {'FINISHED'}
