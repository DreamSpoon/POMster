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
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "Material Node Editor -> Tools -> POMster,  3DView -> Tools -> POMster",
    "category": "Shader Nodes",
    "wiki_url": "",
}

import math

import bpy

from .heightmap_nodes import POMSTER_AddPOMsterToSelectedNode
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
        box.label(text="Create POM Nodes")
        box.operator("pomster.create_pom_uv")
        sub_box = box.box()
        sub_box.prop(scn, "POMSTER_NumSamples")
        sub_box.prop(scn, "POMSTER_SharpenCycles")
        sub_box.prop(scn, "POMSTER_SharpenFactor")
        sub_box = box.box()
        box.label(text="Options")
        sub_box.prop(scn, "POMSTER_UV_InputIndex")
        sub_box.prop(scn, "POMSTER_HeightOutputIndex")
        sub_box.prop(scn, "POMSTER_NodesOverrideCreate")

class POMSTER_PT_FlipUV(bpy.types.Panel):
    bl_label = "Flip UV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Create VU Map from UV Map")
        box.operator("pomster.create_vu_from_uv")

classes = [
    POMSTER_PT_Main,
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

    del bts.POMSTER_SharpenFactor
    del bts.POMSTER_SharpenCycles
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
    bts.POMSTER_SharpenCycles = bp.IntProperty(name="Sharpen Cycles", description="Number of repetitions of the " +
        "Sharpen nodegroup to create to reduce error/warping in final result of POM", default=1, min=1)
    bts.POMSTER_SharpenFactor = bp.FloatProperty(name="Sharpen Factor", description="Sharpen mix factor of new vs " +
        "old sample. 1 is maximum sharpen, which uses only Sharpen POM values and ignores previous height sample " +
        "values. 0 is minimum sharpen, which uses only previous height sample values", default=0.75, min=0.0, max=1.0)

if __name__ == "__main__":
    register()
