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

import math

import bpy

from .node_other import (ensure_node_group, ensure_node_groups, MAT_NG_NAME_SUFFIX)

OPTIMUM_RAY_TYPE_MAT_NG_NAME = "OptimumRayType" + MAT_NG_NAME_SUFFIX
OPTIMUM_RAY_LENGTH_MAT_NG_NAME = "OptimumRayLength" + MAT_NG_NAME_SUFFIX
OPTIMUM_RAY_ANGLE_MAT_NG_NAME = "OptimumRayAngle" + MAT_NG_NAME_SUFFIX
COMBINE_OPTIMUM_TLA_MAT_NG_NAME = "CombineOptimumTLA" + MAT_NG_NAME_SUFFIX

UTIL_ORTHO_TANGENT_NODE_GROUP_NAME = "UtilOrthoTangent"

def create_prereq_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        uv_axes_str = custom_data["uv_axes_str"]
        if node_group_name == OPTIMUM_RAY_TYPE_MAT_NG_NAME:
            return create_mat_ng_optimum_ray_type()
        elif node_group_name == OPTIMUM_RAY_LENGTH_MAT_NG_NAME:
            return create_mat_ng_optimum_ray_length()
        elif node_group_name == OPTIMUM_RAY_ANGLE_MAT_NG_NAME:
            return create_mat_ng_optimum_ray_angle()
        elif node_group_name == COMBINE_OPTIMUM_TLA_MAT_NG_NAME:
            return create_mat_ng_combine_optimum_tla()
        elif uv_axes_str != None and node_group_name == \
                UTIL_ORTHO_TANGENT_NODE_GROUP_NAME + uv_axes_str + MAT_NG_NAME_SUFFIX:
            return create_mat_ng_util_ortho_tangent(custom_data)

    # error
    print("Unknown name passed to create utility node group: " + str(node_group_name))
    return None

def create_mat_ng_util_ortho_tangent(custom_data):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=UTIL_ORTHO_TANGENT_NODE_GROUP_NAME+
        custom_data["uv_axes_str"]+MAT_NG_NAME_SUFFIX, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Position")
    new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Rotate Center")
    if custom_data["uv_axes_str"] == "XY":
        new_node_group.inputs.new(type='NodeSocketFloatAngle', name="Rotate Angle Z")
    elif custom_data["uv_axes_str"] == "XZ":
        new_node_group.inputs.new(type='NodeSocketFloatAngle', name="Rotate Angle Y")
    else:
        new_node_group.inputs.new(type='NodeSocketFloatAngle', name="Rotate Angle X")
    new_node_group.outputs.new(type='NodeSocketVector', name="UV")
    new_node_group.outputs.new(type='NodeSocketVector', name="Tangent U")
    new_node_group.outputs.new(type='NodeSocketVector', name="Tangent V")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (60, 280)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    new_nodes["Vector Rotate.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (60, -20)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    new_nodes["Vector Rotate.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (60, -360)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    new_nodes["Vector Rotate.003"] = node

    # tangent U
    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-120, -100)
    if custom_data["uv_axes_str"] == "XY":
        node.inputs[0].default_value = 0.000000
        node.inputs[1].default_value = -1.000000
        node.inputs[2].default_value = 0.000000
    elif custom_data["uv_axes_str"] == "XZ":
        node.inputs[0].default_value = 0.000000
        node.inputs[1].default_value = 0.000000
        node.inputs[2].default_value = -1.000000
    elif custom_data["uv_axes_str"] == "YZ":
        node.inputs[0].default_value = 0.000000
        node.inputs[1].default_value = 0.000000
        node.inputs[2].default_value = -1.000000
    new_nodes["Combine XYZ"] = node

    # tangent V
    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-120, -440)
    if custom_data["uv_axes_str"] == "XY":
        node.inputs[0].default_value = 1.000000
        node.inputs[1].default_value = 0.000000
        node.inputs[2].default_value = 0.000000
    elif custom_data["uv_axes_str"] == "XZ":
        node.inputs[0].default_value = 1.000000
        node.inputs[1].default_value = 0.000000
        node.inputs[2].default_value = 0.000000
    elif custom_data["uv_axes_str"] == "YZ":
        node.inputs[0].default_value = 0.000000
        node.inputs[1].default_value = 1.000000
        node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Tangent U"
    node.location = (240, 60)
    node.operation = "CROSS_PRODUCT"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Tangent V"
    node.location = (240, -180)
    node.operation = "CROSS_PRODUCT"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-680, -80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (440, 100)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Rotate.001"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Rotate.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Rotate.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Rotate.002"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Rotate.002"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.002"].outputs[0], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Rotate.003"].inputs[3])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Rotate.003"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.003"].outputs[0], new_nodes["Vector Math.004"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_util_ortho_tangents(node_tree, override_create, uv_axes_str):
    node_grp_name = UTIL_ORTHO_TANGENT_NODE_GROUP_NAME + uv_axes_str + MAT_NG_NAME_SUFFIX
    ensure_node_group(override_create, node_grp_name, "ShaderNodeTree", create_prereq_node_group,
                      {"uv_axes_str": uv_axes_str} )
    rotate_axis_letter = ""
    if uv_axes_str == "XY":
        rotate_axis_letter = "Z"
    elif uv_axes_str == "XZ":
        rotate_axis_letter = "Y"
    else:
        rotate_axis_letter = "X"

    offset = (node_tree.view_center[0]/2.5, node_tree.view_center[1]/2.5)

    # deselect all nodes in the node tree
    for n in node_tree.nodes: n.select = False

    new_nodes = {}
    tree_nodes = node_tree.nodes

    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (offset[0], offset[1])
    node.node_tree = bpy.data.node_groups.get(node_grp_name)
    # make this node the active node
    node_tree.nodes.active = node
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (offset[0], offset[1]-280)
    new_nodes["Geometry.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Degrees to Radians " + rotate_axis_letter
    node.hide = True
    node.location = (offset[0], offset[1]-520)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = math.pi / 180.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Rotate Degrees " + rotate_axis_letter
    node.location = (offset[0], offset[1]-560)
    node.outputs[0].default_value = 0.0
    new_nodes["Value.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.label = "Rotate Normal Map " + rotate_axis_letter
    node.location = (offset[0]+360, offset[1]-280)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[4].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.001"] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Geometry.002"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Geometry.002"].outputs[1], new_nodes["Group.002"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group.002"].inputs[3])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Vector Rotate.001"].inputs[3])
    tree_links.new(new_nodes["Value.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Geometry.002"].outputs[1], new_nodes["Vector Rotate.001"].inputs[2])

class POMSTER_AddUtilOrthoTangentNodes(bpy.types.Operator):
    bl_description = "Add nodes to get U / V tangents based on orthographic texture projection. Use this to " \
        "get procedural U and V tangents for e.g. landscape / terrain. Also allows for rotation of UV coordinates " \
        "without breaking Parallax Map"
    bl_idname = "pomster.create_util_orthographic_tangent_nodes"
    bl_label = "Ortho Tangents"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility XY Orthographic Tangents nodes because current " +
                        "material doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        scn = context.scene
        create_util_ortho_tangents(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate, scn.POMSTER_UV_Axes)
        return {'FINISHED'}

def create_mat_ng_optimum_ray_type():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=OPTIMUM_RAY_TYPE_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.outputs.new(type='NodeSocketFloat', name="Type Factor")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 160)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 0)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeLightPath")
    node.location = (0, -160)
    new_nodes["Light Path"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 320)
    node.operation = "ADD"
    node.use_clamp = True
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-220, 320)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (200, 320)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Light Path"].outputs[5], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Light Path"].outputs[6], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Light Path"].outputs[3], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Light Path"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_util_optimum_ray_type(node_tree, override_create):
    ensure_node_group(override_create, OPTIMUM_RAY_TYPE_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    # deselect all nodes in the node tree
    for n in node_tree.nodes: n.select = False

    # create nodes
    tree_nodes = node_tree.nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(OPTIMUM_RAY_TYPE_MAT_NG_NAME)

    # make new node the active node
    node_tree.nodes.active = node

class POMSTER_CreateUtilOptimumRayTypeNode(bpy.types.Operator):
    bl_description = "Add nodes reduce render times (Cycles 'Mix Shader' only) by applying POM effect to only " \
        "these light ray types: Camera, Glossy, Reflection, Transmission"
    bl_idname = "pomster.create_util_optimum_ray_type_node"
    bl_label = "Optimum Ray Type"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Optimum Ray Type nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        scn = context.scene
        create_util_optimum_ray_type(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_mat_ng_optimum_ray_length():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=OPTIMUM_RAY_LENGTH_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Length Add")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Length Multiply")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Mix Shader Fac")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -160)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeLightPath")
    node.location = (60, -320)
    new_nodes["Light Path"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, 160)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    node.inputs[0].default_value = 1.0
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-120, -160)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (240, 160)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Light Path"].outputs[7], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.001"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_util_optimum_ray_length(node_tree, override_create):
    ensure_node_group(override_create, OPTIMUM_RAY_LENGTH_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    # deselect all nodes in the node tree
    for n in node_tree.nodes: n.select = False

    # create nodes
    tree_nodes = node_tree.nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(OPTIMUM_RAY_LENGTH_MAT_NG_NAME)
    node.inputs[0].default_value = -1.0
    node.inputs[1].default_value = 0.03

    # make new node the active node
    node_tree.nodes.active = node

class POMSTER_AddUtilOptimumRayLengthNode(bpy.types.Operator):
    bl_description = "Add nodes reduce render times (Cycles 'Mix Shader' only) by optimizing use of POM by " \
        "distance - farther areas do not have POM effect applied"
    bl_idname = "pomster.create_util_optimum_ray_length_node"
    bl_label = "Optimum Ray Length"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Optimum Distance nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        scn = context.scene
        create_util_optimum_ray_length(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_mat_ng_optimum_ray_angle():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=OPTIMUM_RAY_ANGLE_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Angle Add")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Angle Multiply")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Value")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, -120)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 40)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 200)
    node.operation = "MULTIPLY"
    node.use_clamp = True
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (0, -260)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (0, -400)
    new_nodes["Geometry"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-180, 40)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (180, 200)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.005"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_util_optimum_ray_angle(node_tree, override_create):
    ensure_node_group(override_create, OPTIMUM_RAY_ANGLE_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    # deselect all nodes in the node tree
    for n in node_tree.nodes: n.select = False

    # create nodes
    tree_nodes = node_tree.nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(OPTIMUM_RAY_ANGLE_MAT_NG_NAME)
    node.inputs[0].default_value = 0.0
    node.inputs[1].default_value = 2.0

    # make new node the active node
    node_tree.nodes.active = node

class POMSTER_AddUtilOptimumRayAngleNode(bpy.types.Operator):
    bl_description = "Add nodes to reduce texture warp as incoming viewing angle of light rays approaches parallel " \
        "to geometry, and reduce render times (Cycles 'Mix Shader' only) because POM effect is not applied to near " \
        "parallel light rays"
    bl_idname = "pomster.create_util_optimum_ray_angle_node"
    bl_label = "Optimum Ray Angle"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Optimum Ray Angle nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        scn = context.scene
        create_util_optimum_ray_angle(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_mat_ng_combine_optimum_tla():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=COMBINE_OPTIMUM_TLA_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Length Add")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Length Multiply")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Angle Add")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Angle Multiply")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Mix Fac")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-260, -180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (100, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, 0)
    node.node_tree = bpy.data.node_groups.get(OPTIMUM_RAY_TYPE_MAT_NG_NAME)
    new_nodes["Group.006"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -100)
    node.node_tree = bpy.data.node_groups.get(OPTIMUM_RAY_LENGTH_MAT_NG_NAME)
    new_nodes["Group.005"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-440, -240)
    node.node_tree = bpy.data.node_groups.get(OPTIMUM_RAY_ANGLE_MAT_NG_NAME)
    new_nodes["Group.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-260, 0)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-620, -200)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (280, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[2])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group.005"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group.006"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.004"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_util_combine_optimum_tla(node_tree, override_create):
    ensure_node_groups(override_create, [ OPTIMUM_RAY_TYPE_MAT_NG_NAME,
                                         OPTIMUM_RAY_LENGTH_MAT_NG_NAME,
                                         OPTIMUM_RAY_ANGLE_MAT_NG_NAME,
                                         COMBINE_OPTIMUM_TLA_MAT_NG_NAME], 'ShaderNodeTree', create_prereq_node_group)

    # deselect all nodes in the node tree
    for n in node_tree.nodes: n.select = False

    new_nodes = {}

    # create nodes
    tree_nodes = node_tree.nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(COMBINE_OPTIMUM_TLA_MAT_NG_NAME)
    node.inputs[0].default_value = -1.000000
    node.inputs[1].default_value = 0.030000
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = 2.000000

    # make new node the active node
    node_tree.nodes.active = node
    new_nodes["CombineOptimumTLA_Group"] = node

    # create mix shader node and link
    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5 + 140)
    new_nodes["Mix Shader"] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["CombineOptimumTLA_Group"].outputs[0], new_nodes["Mix Shader"].inputs[0])

class POMSTER_AddUtilCombineOptimumTLA_Node(bpy.types.Operator):
    bl_description = "Add a node to combine the Optimum Ray Type/Length/Angle together"
    bl_idname = "pomster.create_util_optimum_combine_tla"
    bl_label = "Combine Optimum TLA"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Combine Optimum TLA node because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        scn = context.scene
        create_util_combine_optimum_tla(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}
