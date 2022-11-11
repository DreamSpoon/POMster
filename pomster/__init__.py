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
    "version": (0, 1, 1),
    "blender": (2, 80, 0),
    "location": "Material Node Editor -> Tools -> POMster,  3DView -> Tools -> POMster",
    "category": "Shader Nodes",
    "wiki_url": "",
}

import math

import bpy

from .mat_nodes.pomster_basic import POMSTER_AddPOMsterBasic
from .mat_nodes.pomster_heightmap import POMSTER_AddPOMsterToSelectedNode
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
        box.label(text="Create Heightmap POM")
        box.operator("pomster.create_heightmap_pom_uv")
        sub_box = box.box()
        sub_box.prop(scn, "POMSTER_NumSamples")
        sub_box.prop(scn, "POMSTER_NumErrorCutoffCycles")
        sub_box.prop(scn, "POMSTER_NumSharpenCycles")
        sub_box = box.box()
        sub_box.label(text="Options")
        sub_box.prop(scn, "POMSTER_UV_InputIndex")
        sub_box.prop(scn, "POMSTER_HeightOutputIndex")
        sub_box.prop(scn, "POMSTER_NodesOverrideCreate")
        sub_box.prop(scn, "POMSTER_EncloseNicely")

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
        row.template_list("MESH_UL_uvmaps", "uvmaps", obj_data, "uv_layers", obj_data.uv_layers, "active_index", rows=2)

classes = [
    POMSTER_PT_Main,
    POMSTER_AddPOMsterBasic,
    POMSTER_AddPOMsterToSelectedNode,
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

    del bts.POMSTER_NumSamples
    del bts.POMSTER_HeightOutputIndex
    del bts.POMSTER_UV_InputIndex
    del bts.POMSTER_NodesOverrideCreate

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props

    bts.POMSTER_NodesOverrideCreate = bp.BoolProperty(name="Override Create", description="Shader Nodes custom " +
        "Node Groups will be re-created if this option is enabled. When custom Node Groups are override created, " +
        "old Node Groups of the same name are renamed and deprecated", default=False)
    bts.POMSTER_UV_InputIndex = bp.IntProperty(name="UV Input Number", description="Choose the input number " +
        "number of the selected node that has the UV coordinates input - usually input #1", default=1, min=1)
    bts.POMSTER_HeightOutputIndex = bp.IntProperty(name="Height Output Number", description="Choose the output " +
        "number of the selected node that has the Height output - usually output #1", default=1, min=1)
    bts.POMSTER_NumSamples = bp.IntProperty(name="Samples", description="Number of spread samples used to " +
        "calculate POM", default=3, min=3)
    bts.POMSTER_NumErrorCutoffCycles = bp.IntProperty(name="Error Cutoff", description="Number of cycles of Error " +
        "Cutoff to use in POM - more samples requires more cycles of Error Cutoff like so: cutoff_cycles = log(2, " +
        "samples)", default=1, min=1)
    bts.POMSTER_NumSharpenCycles = bp.IntProperty(name="Sharpen Cycles", description="Number of repetitions of the " +
        "Sharpen nodegroup to create to reduce error/warping in final result of POM", default=1, min=1)
    bts.POMSTER_UVtoVUmapConvertAll = bp.BoolProperty(name="All UV Maps", description="Make VU Maps for all UV Maps " +
        "of selected object, instead of only selected UV Map", default=False)
    bts.POMSTER_EncloseNicely = bp.BoolProperty(name="Enclose Nicely", description="Enclose the POM node setup in a " +
        "nodegroup, to make it nicer to look at / easier to use", default=True)

if __name__ == "__main__":
    register()
