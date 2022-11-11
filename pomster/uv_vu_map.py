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

import bpy

def create_vu_from_uv_map(obj, convert_all):
    # make copy of refs to UV layers (UV maps), because this list will change as it's refs are iterated over
    uv_layers_copy = [uvl for uvl in obj.data.uv_layers]
    # convert all UV layers
    if convert_all:
        for uv_layer in uv_layers_copy:
            new_uv_map = obj.data.uv_layers.new(name="VUMap." + uv_layer.name)
            # iterate through all UV pairs in the map, switching the U and V values
            for loop in obj.data.loops:
                # get original (U, V) coordinates
                uv_coords = uv_layer.data[loop.index].uv
                # store the original (U, V) coordinates as (V, U) coordinates
                new_uv_map.data[loop.index].uv = (uv_coords[1], uv_coords[0])
    # convert only the active UV layer
    else:
        active_uv_map = obj.data.uv_layers.active
        new_uv_map = obj.data.uv_layers.new(name="VUMap." + active_uv_map.name)
        # iterate through all UV pairs in the map, switching the U and V values
        for loop in obj.data.loops:
            # get original (U, V) coordinates
            uv_coords = active_uv_map.data[loop.index].uv
            # store the original (U, V) coordinates as (V, U) coordinates
            new_uv_map.data[loop.index].uv = (uv_coords[1], uv_coords[0])

class POMSTER_CreateVUMap(bpy.types.Operator):
    bl_description = "Copy the given UV map to a second map, with the U and V values switched, so that second map " \
        "is a VU map"
    bl_idname = "pomster.create_vu_from_uv"
    bl_label = "U-V Map to V-U Map"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object != None and context.active_object.type == 'MESH'

    def execute(self, context):
        scn = context.scene
        create_vu_from_uv_map(context.active_object, scn.POMSTER_UVtoVUmapConvertAll)
        return {'FINISHED'}
