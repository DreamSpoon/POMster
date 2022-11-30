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

from .node_other import (ensure_node_group, MAT_NG_NAME_SUFFIX)

CUBE_MASK_MAT_NG_NAME = "CubeMask" + MAT_NG_NAME_SUFFIX
SPHERE_MASK_MAT_NG_NAME = "SphereMask" + MAT_NG_NAME_SUFFIX

def create_prereq_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == CUBE_MASK_MAT_NG_NAME:
            return create_mat_ng_cube_mask()
        elif node_group_name == SPHERE_MASK_MAT_NG_NAME:
            return create_mat_ng_sphere_mask()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_mat_ng_cube_mask():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=CUBE_MASK_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Test Position")
    new_node_group.inputs.new(type='NodeSocketVector', name="Cube Location")
    new_node_group.inputs.new(type='NodeSocketVectorEuler', name="Cube Rotation")
    new_node_group.inputs.new(type='NodeSocketVector', name="Cube Scale")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-60, -20)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (300, -100)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (120, -60)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, 60)
    node.operation = "DISTANCE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (480, -20)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -120)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -240)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -360)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -240)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (-1.0, -1.0, -1.0)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, -360)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (2.0, 2.0, 2.0)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-620, -100)
    node.invert = True
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-800, -100)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1020, -220)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (860, 60)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.001"].outputs[1], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Map Range"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Map Range.001"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Map Range.001"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Map Range.001"].inputs[3])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Map Range.001"].inputs[4])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Map Range.002"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Map Range.002"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Map Range.002"].inputs[3])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Map Range.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.002"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_cube_shader_mask_node(node_tree, override_create):
    ensure_node_group(override_create, CUBE_MASK_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes
    for n in tree_nodes: n.select = False

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(CUBE_MASK_MAT_NG_NAME)
    node.inputs[3].default_value = (1.0, 1.0, 1.0)
    # set this node to be active node
    node_tree.nodes.active = node

class POMSTER_AddCubeMask(bpy.types.Operator):
    bl_description = "Add a Cube Shader Mask node, which gives Distance value 0 when inside the cube, or the " \
        "distance from the cube if outside the cube"
    bl_idname = "pomster.create_cube_shader_mask_node"
    bl_label = "Cube Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Cube Shader Mask nodebecause current material doesn't use " +
                        "nodes.  Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_cube_shader_mask_node(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_mat_ng_sphere_mask():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SPHERE_MASK_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Test Position")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Sphere Location")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-640, -120)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-460, -120)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, -120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-820, -120)
    node.operation = "DISTANCE"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1020, -220)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-100, -120)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_sphere_shader_mask_node(node_tree, override_create):
    ensure_node_group(override_create, SPHERE_MASK_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes
    for n in tree_nodes: n.select = False

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(SPHERE_MASK_MAT_NG_NAME)
    node.inputs[1].default_value = 1.0
    # set this node to be active node
    node_tree.nodes.active = node

class POMSTER_AddSphereMask(bpy.types.Operator):
    bl_description = "Add a Sphere Shader Mask node, which gives Distance value 0 when inside the sphere, or the " \
        "distance from the sphere if outside the sphere"
    bl_idname = "pomster.create_sphere_shader_mask_node"
    bl_label = "Sphere Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Sphere Shader Mask nodebecause current material doesn't use " +
                        "nodes.  Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_sphere_shader_mask_node(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}
