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
    "version": (0, 6, 0),
    "blender": (2, 80, 0),
    "location": "Node Editor -> Tools -> POMster,  3DView -> Tools -> POMster",
    "category": "Shader Nodes, Geometry Nodes",
    "wiki_url": "https://github.com/DreamSpoon/POMster#readme",
}

import math

import bpy
from bpy.types import PropertyGroup
from bpy.props import (BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty)

from .mat_nodes.parallax_map import POMSTER_AddParallaxMapNode
from .mat_nodes.utility import (POMSTER_AddUtilOrthoTangentNodes, POMSTER_CreateUtilOptimumRayTypeNode,
    POMSTER_AddUtilOptimumRayLengthNode, POMSTER_AddUtilOptimumRayAngleNode, POMSTER_AddUtilCombineOptimumTLA_Node)
from .mat_nodes.offset_conestep_pom import POMSTER_AddOCPOM_Node
from .mat_nodes.shader_mask import (POMSTER_AddCubeMask, POMSTER_AddSphereMask, POMSTER_AddMaskObjLocRotSclNodes)
from .geo_nodes.shell_fringe import (POMSTER_AddShellArrayNode, POMSTER_AddFringeExtrudeNode)
from .mat_nodes.shell_fringe_blend import POMSTER_AddShellFringeBlendNode
from .uv_vu_map import POMSTER_CreateVUMap
from .obj_grid_snap import (POMSTER_AddObjGridSnap, GRID_SIZE_CPROP_NAME)
from .obj_shell_fringe import POMSTER_CreateObjModShellFringe

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
        o_data = None
        if context.object != None:
            o_data = context.object.data
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.active = o_data != None
        col.label(text="Create VU Map from UV Map")
        col.operator("pomster.create_vu_from_uv")
        col.label(text="Select UV Map")
        col.prop(scn.POMster, "uv_to_vu_map_convert_all")
        if o_data != None and hasattr(o_data, "uv_layers"):
            r = col.row()
            r.active = not scn.POMster.uv_to_vu_map_convert_all
            r.template_list("MESH_UL_uvmaps", "uvmaps", o_data, "uv_layers", o_data.uv_layers, "active_index", rows=2)

class POMSTER_PT_ObjectGridSnap(bpy.types.Panel):
    bl_label = "Object Grid Snap"
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

class POMSTER_PT_ObjectShellFringe(bpy.types.Panel):
    bl_label = "Shell and Fringe"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "POMster"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        box = layout.box()
        box.label(text="Parallax Shell and Fringe")
        box.operator("pomster.add_object_shell_fringe")
        box.prop(scn.POMster, "default_height_multiplier")

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
        sub_box.prop(scn.POMster, "uv_axes")
        box = layout.box()
        box.prop(scn.POMster, "nodes_override_create")

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
        sub_box.prop(scn.POMster, "num_samples")
        sub_box = box.box()
        sub_box.label(text="Height (Displacement) Texture")
        sub_box.prop(scn.POMster, "height_img_input", text="")
        sub_box.prop(scn.POMster, "default_height_multiplier")
        sub_box.prop(scn.POMster, "ocpom_mapping_nodes")
        sub_box = box.box()
        sub_box.label(text="Custom Node Input")
        sub_box.prop(scn.POMster, "uv_input_index")
        sub_box.label(text="Custom Node Output")
        sub_box.prop(scn.POMster, "height_output_index")
        sub_box.prop(scn.POMster, "cone_ratio_angle_output_index")
        sub_box.prop(scn.POMster, "cone_ratio_divisor_output_index")
        sub_box.prop(scn.POMster, "cone_offset_output_index")
        box = layout.box()
        box.prop(scn.POMster, "nodes_override_create")

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
        box.prop(scn.POMster, "nodes_override_create")

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
        box.prop(scn.POMster, "mask_input_object")
        box = layout.box()
        box.prop(scn.POMster, "nodes_override_create")

class POMSTER_PT_NodeShellFringe(bpy.types.Panel):
    bl_label = "Shell and Fringe"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "POMster"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        box = layout.box()
        box.label(text="Geometry Nodes")
        box.operator("pomster.create_shell_array_node")
        box.operator("pomster.create_fringe_extrude_node")
        box.label(text="Shader Nodes")
        box.operator("pomster.create_shell_fringe_blend_node")
        box.prop(scn.POMster, "add_shell_fringe_inputs")
        col = box.column()
        col.active = scn.POMster.add_shell_fringe_inputs
        col.prop(scn.POMster, "base_color_img_input")
        col.prop(scn.POMster, "normal_img_input")
        col.prop(scn.POMster, "height_img_input")
        box = layout.box()
        box.prop(scn.POMster, "nodes_override_create")

class POMsterPropGrp(PropertyGroup):
    num_samples: IntProperty(name="Samples", description="Number of samples used to calculate POM", default=8, min=1)
    nodes_override_create: BoolProperty(name="Override Create", description="Shader Nodes custom Node Groups will " +
        "be re-created if this option is enabled. When custom Node Groups are override created, old Node Groups of " +
        "the same name are renamed and deprecated", default=False)
    uv_input_index: IntProperty(name="UV Input Number", description="Choose the input number number of the " +
        "selected node that has the UV coordinates input - usually input #1", default=1, min=1)
    height_output_index: IntProperty(name="Height Output Number", description="Choose the output number of the " +
        "active node that has the Height output - usually output #1", default=1, min=1)
    cone_ratio_angle_output_index: IntProperty(name="Cone Ratio Angle Output Number", description="Choose output " +
        "number of active node for Cone Ratio Angle output - usually output #2. Value range is 0 to 1 inclusive, " +
        "re: 0 to 90 degrees angle. Value of 0 is zero conestep, value of 1 is full conestep", default=2, min=1)
    cone_ratio_divisor_output_index: IntProperty(name="Cone Ratio Divisor Output Number", description="Choose " +
        "output number of active node for Cone Ratio Divisor output - usually output #3", default=3, min=1)
    cone_offset_output_index: IntProperty(name="Cone Offset Output Number", description="Choose output number of " +
        "active node for Cone Offset output - usually output #4. Value range is same as Height output", default=4,
        min=1)
    uv_to_vu_map_convert_all: BoolProperty(name="All UV Maps", description="Make VU Maps for all UV Maps of " +
        "selected object, instead of only selected UV Map", default=False)
    uv_axes: EnumProperty(name= "UV axes", description= "Axes to use for UV input", items=UV_ORTHO_AXES_ENUM_ITEMS)
    mask_input_object: PointerProperty(name="Object", description="Input nodes for location, rotation, scale will " +
        "get their values from this Object", type=bpy.types.Object)
    add_shell_fringe_inputs: BoolProperty(name="Add Shell Fringe Inputs", description="When Shell Fringe Blend " +
        "node is created, add input nodes create a simple default setup", default=True)
    base_color_img_input: PointerProperty(name="Base Color", description="Image texture for base color (albedo)",
        type=bpy.types.Image)
    normal_img_input: PointerProperty(name="Normal", description="Image texture for surface normal",
        type=bpy.types.Image)
    height_img_input: PointerProperty(name="Height", description="Image texture for height (displacement)",
        type=bpy.types.Image)
    default_height_multiplier: FloatProperty(name="Height Multiplier", description="Height (Displacement) " +
        "texture's value is multiplied by Height Multiplier", default=0.05, min=0)
    ocpom_mapping_nodes: BoolProperty(name="Mapping Nodes", description="Add UV mapping nodes for Location, " +
        "Rotation, Scale when OCPOM node inputs are created", default=True)

classes = [
    POMSTER_PT_FlipUV,
    POMSTER_CreateVUMap,
    POMSTER_PT_ObjectGridSnap,
    POMSTER_AddObjGridSnap,
    POMSTER_PT_ObjectShellFringe,
    POMSTER_CreateObjModShellFringe,
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
    POMSTER_PT_NodeShellFringe,
    POMSTER_AddShellArrayNode,
    POMSTER_AddFringeExtrudeNode,
    POMSTER_AddShellFringeBlendNode,
    POMsterPropGrp,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.POMster = PointerProperty(type=POMsterPropGrp)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.POMster

if __name__ == "__main__":
    register()
