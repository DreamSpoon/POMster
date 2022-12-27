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
    "version": (0, 4, 0),
    "blender": (2, 80, 0),
    "location": "Material Node Editor -> Tools -> POMster,  3DView -> Tools -> POMster",
    "category": "Shader Nodes",
    "wiki_url": "",
}

import math

import bpy

from .mat_nodes.parallax_map import POMSTER_AddParallaxMapNode
from .mat_nodes.utility import (POMSTER_AddUtilOrthoTangentNodes, POMSTER_CreateUtilOptimumRayTypeNode,
    POMSTER_AddUtilOptimumRayLengthNode, POMSTER_AddUtilOptimumRayAngleNode, POMSTER_AddUtilCombineOptimumTLA_Node)
from .mat_nodes.offset_conestep_pom import POMSTER_AddOCPOM_Node
from .mat_nodes.shader_mask import (POMSTER_AddCubeMask, POMSTER_AddSphereMask, POMSTER_AddMaskObjLocRotSclNodes)
from .obj_grid_snap import (POMSTER_AddObjGridSnap, GRID_SIZE_CPROP_NAME)
from .uv_vu_map import POMSTER_CreateVUMap

UV_ORTHO_AXES_ENUM_ITEMS = [
    ("XY", "XY", ""),
    ("XZ", "XZ", ""),
    ("YZ", "YZ", ""),
]

class POMSTER_PT_FlipUV(bpy.types.Panel):
    bl_label = "Flip UV"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        scn = context.scene
        obj_data = None
        if context.object != None:
            obj_data = context.object.data
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.active = obj_data != None
        col.label(text="Create VU Map from UV Map")
        col.operator("pomster.create_vu_from_uv")
        col.label(text="Select UV Map")
        col.prop(scn, "POMSTER_UVtoVUmapConvertAll")
        if obj_data != None and hasattr(obj_data, "uv_layers"):
            r = col.row()
            r.active = not scn.POMSTER_UVtoVUmapConvertAll
            r.template_list("MESH_UL_uvmaps", "uvmaps", obj_data, "uv_layers", obj_data.uv_layers, "active_index",
                            rows=2)

class POMSTER_PT_ObjectGridSnap(bpy.types.Panel):
    bl_label = "ObjectGridSnap"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Snap Object Location to Grid")
        box.operator("pomster.add_object_grid_snap")
        if context.active_object != None:
            grid_size_cprop = context.active_object.get(GRID_SIZE_CPROP_NAME)
            if grid_size_cprop != None:
                box.label(text="Active Object's Grid Snap")
                box.prop(context.active_object, "[\""+GRID_SIZE_CPROP_NAME+"\"]", text="")

class POMSTER_PT_General(bpy.types.Panel):
    bl_label = "Parallax Map"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        sub_box = box.box()
        sub_box.operator("pomster.create_parallax_map_node")
        sub_box = box.box()
        sub_box.label(text="Landscape / Procedural Tangent")
        sub_box.operator("pomster.create_util_orthographic_tangent_nodes")
        sub_box.prop(scn, "POMSTER_UV_Axes")
        box = layout.box()
        box.prop(scn, "POMSTER_NodesOverrideCreate")

class POMSTER_PT_OCPOM(bpy.types.Panel):
    bl_label = "OCPOM"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "POMster"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        box.label(text="Create Nodes")
        sub_box = box.box()
        sub_box.operator("pomster.create_offset_conestep_pom_nodes")
        sub_box.prop(scn, "POMSTER_NumSamples")
        sub_box = box.box()
        sub_box.label(text="Custom Node Input")
        sub_box.prop(scn, "POMSTER_UV_InputIndex")
        sub_box.label(text="Custom Node Output")
        sub_box.prop(scn, "POMSTER_DepthOutputIndex")
        sub_box.prop(scn, "POMSTER_ConeRatioAngleOutputIndex")
        sub_box.prop(scn, "POMSTER_ConeRatioDivisorOutputIndex")
        sub_box.prop(scn, "POMSTER_ConeOffsetOutputIndex")
        box = layout.box()
        box.prop(scn, "POMSTER_NodesOverrideCreate")

class POMSTER_PT_Optimize(bpy.types.Panel):
    bl_label = "Optimize"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "POMster"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        sub_box = box.box()
        sub_box.label(text="Reduce Cycles Render Time")
        sub_box.operator("pomster.create_util_optimum_ray_type_node")
        sub_box.operator("pomster.create_util_optimum_ray_length_node")
        sub_box = box.box()
        sub_box.label(text="Reduce Texture Warp")
        sub_box.operator("pomster.create_util_optimum_ray_angle_node")
        sub_box = box.box()
        sub_box.label(text="Combine Optimum")
        sub_box.operator("pomster.create_util_optimum_combine_tla")
        box = layout.box()
        box.prop(scn, "POMSTER_NodesOverrideCreate")

class POMSTER_PT_ShaderMask(bpy.types.Panel):
    bl_label = "Shader Mask"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "POMster"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        box = layout.box()
        box.label(text="Mask")
        box.operator("pomster.create_cube_shader_mask_node")
        box.operator("pomster.create_sphere_shader_mask_node")
        box = layout.box()
        box.label(text="Object Loc, Rot, Scl")
        box.operator("pomster.create_mask_object_loc_rot_scl_nodes")
        box.prop(scn, "POMSTER_MaskInputObject")
        box = layout.box()
        box.prop(scn, "POMSTER_NodesOverrideCreate")

classes = [
    POMSTER_PT_FlipUV,
    POMSTER_PT_ObjectGridSnap,
    POMSTER_AddObjGridSnap,
    POMSTER_CreateVUMap,
    POMSTER_PT_General,
    POMSTER_AddParallaxMapNode,
    POMSTER_AddUtilOrthoTangentNodes,
    POMSTER_PT_OCPOM,
    POMSTER_AddOCPOM_Node,
    POMSTER_PT_Optimize,
    POMSTER_CreateUtilOptimumRayTypeNode,
    POMSTER_AddUtilOptimumRayLengthNode,
    POMSTER_AddUtilOptimumRayAngleNode,
    POMSTER_AddUtilCombineOptimumTLA_Node,
    POMSTER_PT_ShaderMask,
    POMSTER_AddCubeMask,
    POMSTER_AddSphereMask,
    POMSTER_AddMaskObjLocRotSclNodes,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_props()

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bts = bpy.types.Scene

    del bts.POMSTER_MaskInputObject
    del bts.POMSTER_UV_Axes
    del bts.POMSTER_UVtoVUmapConvertAll
    del bts.POMSTER_ConeOffsetOutputIndex
    del bts.POMSTER_ConeRatioDivisorOutputIndex
    del bts.POMSTER_ConeRatioAngleOutputIndex
    del bts.POMSTER_DepthOutputIndex
    del bts.POMSTER_UV_InputIndex
    del bts.POMSTER_NodesOverrideCreate
    del bts.POMSTER_NumSamples

def register_props():
    bts = bpy.types.Scene
    bp = bpy.props

    bts.POMSTER_NumSamples = bp.IntProperty(name="Samples", description="Number of samples used to " +
        "calculate POM", default=8, min=1)
    bts.POMSTER_NodesOverrideCreate = bp.BoolProperty(name="Override Create", description="Shader Nodes custom " +
        "Node Groups will be re-created if this option is enabled. When custom Node Groups are override created, " +
        "old Node Groups of the same name are renamed and deprecated", default=False)
    bts.POMSTER_UV_InputIndex = bp.IntProperty(name="UV Input Number", description="Choose the input number " +
        "number of the selected node that has the UV coordinates input - usually input #1", default=1, min=1)
    bts.POMSTER_DepthOutputIndex = bp.IntProperty(name="Depth Output Number", description="Choose the output " +
        "number of the active node that has the Depth output - usually output #1", default=1, min=1)
    bts.POMSTER_ConeRatioAngleOutputIndex = bp.IntProperty(name="Cone Ratio Angle Output Number",
        description="Choose output number of active node for Cone Ratio Angle output - usually output #2. Value range"+
        " is 0 to 1 inclusive, re: 0 to 90 degrees angle. Value of 0 is zero conestep, value of 1 is full conestep",
        default=2, min=1)
    bts.POMSTER_ConeRatioDivisorOutputIndex = bp.IntProperty(name="Cone Ratio Divisor Output Number",
        description="Choose output number of active node for Cone Ratio Divisor output - usually output #3",
        default=3, min=1)
    bts.POMSTER_ConeOffsetOutputIndex = bp.IntProperty(name="Cone Offset Output Number",
        description="Choose output number of active node for Cone Offset output - usually output #4. Value range " +
        "is same as Depth output", default=4, min=1)
    bts.POMSTER_UVtoVUmapConvertAll = bp.BoolProperty(name="All UV Maps", description="Make VU Maps for all UV Maps " +
        "of selected object, instead of only selected UV Map", default=False)
    bts.POMSTER_UV_Axes = bp.EnumProperty(name= "UV axes", description= "Axes to use for UV input",
        items=UV_ORTHO_AXES_ENUM_ITEMS)
    bts.POMSTER_MaskInputObject = bp.PointerProperty(name="Object", description="Input nodes for location, " +
        "rotation, scale will get their values from this Object", type=bpy.types.Object)

if __name__ == "__main__":
    register()
