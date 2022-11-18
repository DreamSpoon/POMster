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

bl_info = {
    "name": "POMster",
    "description": "Parallax Occlusion Map(ster) for holographic texture effects.",
    "author": "Dave",
    "version": (0, 2, 1),
    "blender": (2, 80, 0),
    "location": "Material Node Editor -> Tools -> POMster,  3DView -> Tools -> POMster",
    "category": "Shader Nodes",
    "wiki_url": "",
}

import math

import bpy

from .mat_nodes.pomster_basic import (POMSTER_AddPOMsterBasic, POMSTER_AddPOMsterUtilOrthoTangents)
from .mat_nodes.offset_conestep_pom import POMSTER_AddOCPOM
from .uv_vu_map import POMSTER_CreateVUMap

class POMSTER_PT_Main(bpy.types.Panel):
    bl_idname = "POMSTER_PT_Main"
    bl_label = "Main"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        box.label(text="Create Basic POM")
        box.operator("pomster.create_basic_pom_uv")
        box = layout.box()
        box.label(text="Create Offset Conestep POM")
        box.operator("pomster.create_offset_conestep_pom")
        box.prop(scn, "POMSTER_NumSamples")
        sub_box = box.box()
        sub_box.label(text="Group Node Input/Output")
        sub_box.prop(scn, "POMSTER_UV_InputIndex")
        sub_box.prop(scn, "POMSTER_HeightOutputIndex")
        sub_box.prop(scn, "POMSTER_ConeRatioOutputIndex")
        sub_box.prop(scn, "POMSTER_ConeOffsetOutputIndex")
        sub_box.label(text="Options")
        sub_box.prop(scn, "POMSTER_NodesOverrideCreate")
        box = layout.box()
        box.label(text="Utility")
        box.operator("pomster.create_util_orthographic_tangents")

class POMSTER_PT_FlipUV(bpy.types.Panel):
    bl_label = "Flip UV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        scn = context.scene
        obj_data = context.object.data
        layout = self.layout
        box = layout.box()
        box.label(text="Create VU Map from UV Map")
        box.operator("pomster.create_vu_from_uv")
        box.label(text="Select UV Map")
        box.prop(scn, "POMSTER_UVtoVUmapConvertAll")
        row = box.row()
        row.active = not scn.POMSTER_UVtoVUmapConvertAll
        row.template_list("MESH_UL_uvmaps", "uvmaps", obj_data, "uv_layers", obj_data.uv_layers, "active_index",
                          rows=2)

classes = [
    POMSTER_PT_Main,
    POMSTER_AddPOMsterBasic,
    POMSTER_AddOCPOM,
    POMSTER_AddPOMsterUtilOrthoTangents,
    POMSTER_PT_FlipUV,
    POMSTER_CreateVUMap,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bts = bpy.types.Scene

    del bts.POMSTER_ConeOffsetOutputIndex
    del bts.POMSTER_ConeRatioOutputIndex
    del bts.POMSTER_HeightOutputIndex
    del bts.POMSTER_UV_InputIndex
    del bts.POMSTER_NodesOverrideCreate
    del bts.POMSTER_NumSamples

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props

    bts.POMSTER_NumSamples = bp.IntProperty(name="Samples", description="Number of spread samples used to " +
        "calculate POM", default=1, min=1)
    bts.POMSTER_NodesOverrideCreate = bp.BoolProperty(name="Override Create", description="Shader Nodes custom " +
        "Node Groups will be re-created if this option is enabled. When custom Node Groups are override created, " +
        "old Node Groups of the same name are renamed and deprecated", default=False)
    bts.POMSTER_UV_InputIndex = bp.IntProperty(name="UV Input Number", description="Choose the input number " +
        "number of the selected node that has the UV coordinates input - usually input #1", default=1, min=1)
    bts.POMSTER_HeightOutputIndex = bp.IntProperty(name="Depth Output Number", description="Choose the output " +
        "number of the active node that has the Depth output - usually output #1", default=1, min=1)
    bts.POMSTER_ConeRatioOutputIndex = bp.IntProperty(name="Cone Ratio Output Number",
        description="Choose output number of active node for Cone Ratio output - usually output #2. Value range is " +
        "0 to 1 inclusive, re: 0 to 90 degrees angle. Value of 0 is zero conestep, value of 1 is full conestep",
        default=2, min=1)
    bts.POMSTER_ConeOffsetOutputIndex = bp.IntProperty(name="Cone Offset Output Number",
        description="Choose output number of active node for Cone Offset output - usually output #3. Value range " +
        "is same as Depth output", default=3, min=1)
    bts.POMSTER_UVtoVUmapConvertAll = bp.BoolProperty(name="All UV Maps", description="Make VU Maps for all UV Maps " +
        "of selected object, instead of only selected UV Map", default=False)

if __name__ == "__main__":
    register()
