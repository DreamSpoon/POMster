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

from ..node_other import (get_tangent_map_name, ensure_node_group, MAT_NG_NAME_SUFFIX)

PARALLAX_MAP_MAT_NG_NAME = "ParallaxMap" + MAT_NG_NAME_SUFFIX

PARALLAX_MAP_NODENAME = "ParallaxMapGrp"
UV_INPUT_NODENAME = "UV Input"
TANGENT_U_INPUT_NODENAME = "Tangent U"
TANGENT_V_INPUT_NODENAME = "Tangent V"
GEOMETRY_INPUT_NODENAME = "Geometry Input"

def create_prereq_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == PARALLAX_MAP_MAT_NG_NAME:
            return create_mat_ng_parallax_map()

def create_mat_ng_parallax_map():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=PARALLAX_MAP_MAT_NG_NAME, type='ShaderNodeTree')
    # remove old group inputs and outputs
    new_node_group.inputs.clear()
    new_node_group.outputs.clear()
    # create new group inputs and outputs
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_input = new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_input.default_value = (1.0, 1.0, 1.0)
    new_input = new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U")
    new_input.default_value = (1.0, 0.0, 0.0)
    new_input = new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V")
    new_input.default_value = (0.0, 1.0, 0.0)
    new_input = new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
    new_input.default_value = (0.0, 0.0, 1.0)
    new_input = new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
    new_input.default_value = (0.0, 0.0, 1.0)
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Height")
    new_input.max_value = 0.000000
    new_node_group.outputs.new(type='NodeSocketVector', name="UV Output")

    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, 40)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (320, 200)
    node.operation = "MULTIPLY"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (500, 200)
    node.operation = "ADD"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (140, 200)
    node.operation = "SCALE"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-40, 200)
    node.operation = "SCALE"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-40, -140)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-40, 40)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, -140)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, -280)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-400, 200)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-220, 200)
    node.inputs[2].default_value = 1.0
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-600, 80)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (680, 200)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Vector Math.006"].outputs[1], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Vector Math.003"].inputs[3])
    tree_links.new(new_nodes["Vector Math.006"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.004"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_parallax_map_nodes(active_obj, node_tree, override_create):
    ensure_node_group(override_create, PARALLAX_MAP_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes in tree before creating new node
    for node in tree_nodes: node.select = False

    new_nodes = {}

    # create a node group node and give it a ref to the POMster UV nodegroup
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (0, 0)
    node.node_tree = bpy.data.node_groups.get(PARALLAX_MAP_MAT_NG_NAME)
    node.inputs[0].default_value = (0, 0, 0)
    node.inputs[1].default_value = (1, 1, 1)
    node.inputs[2].default_value = (1, 0, 0)
    node.inputs[3].default_value = (0, 1, 0)
    node.inputs[4].default_value = (0, 0, 1)
    node.inputs[5].default_value = (0, 0, 1)
    node.inputs[6].default_value = 0.0
    node.select = True
    # make new node the active node
    tree_nodes.active = node
    new_nodes[PARALLAX_MAP_NODENAME] = node

    # create nodes for OCPOM input
    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-220, 160)
    new_nodes[UV_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = TANGENT_U_INPUT_NODENAME
    node.location = (-220, -100)
    node.direction_type = "UV_MAP"
    node.uv_map = get_tangent_map_name("U", active_obj)
    new_nodes[TANGENT_U_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = TANGENT_V_INPUT_NODENAME
    node.location = (-220, -200)
    node.direction_type = "UV_MAP"
    node.uv_map = get_tangent_map_name("V", active_obj)
    new_nodes[TANGENT_V_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (-220, -300)
    new_nodes[GEOMETRY_INPUT_NODENAME] = node

    # offset node locations relative to view center
    view_center = (node_tree.view_center[0] / 1.5, node_tree.view_center[1] / 1.5)
    for n in new_nodes.values():
        n.location = (n.location[0] + view_center[0], n.location[1] + view_center[1])

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes[UV_INPUT_NODENAME].outputs[2], new_nodes[PARALLAX_MAP_NODENAME].inputs[0])
    tree_links.new(new_nodes[TANGENT_U_INPUT_NODENAME].outputs[0], new_nodes[PARALLAX_MAP_NODENAME].inputs[2])
    tree_links.new(new_nodes[TANGENT_V_INPUT_NODENAME].outputs[0], new_nodes[PARALLAX_MAP_NODENAME].inputs[3])
    tree_links.new(new_nodes[GEOMETRY_INPUT_NODENAME].outputs[1], new_nodes[PARALLAX_MAP_NODENAME].inputs[4])
    tree_links.new(new_nodes[GEOMETRY_INPUT_NODENAME].outputs[4], new_nodes[PARALLAX_MAP_NODENAME].inputs[5])

class POMSTER_AddParallaxMapNode(bpy.types.Operator):
    bl_description = "Add a Parallax Map node, which can be used to add 'depth' effect to materials"
    bl_idname = "pomster.create_parallax_map_node"
    bl_label = "Parallax Map"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Parallax Occlusion Map node because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_parallax_map_nodes(context.active_object, context.space_data.edit_tree, scn.POMster.nodes_override_create)
        return {'FINISHED'}
