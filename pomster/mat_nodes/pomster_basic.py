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

from .node_other import ensure_node_group
from .mat_ng_pomster import (create_mat_ng_pomster, POMSTER_UV_MAT_NG_NAME)

def create_prereq_util_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == POMSTER_UV_MAT_NG_NAME:
            return create_mat_ng_pomster()

def create_pom_basic_nodes(node_tree, override_create):
    ensure_node_group(override_create, POMSTER_UV_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_util_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes in tree before creating new node
    for node in tree_nodes: node.select = False

    # create a node group node and give it a ref to the POMster UV nodegroup
    node = tree_nodes.new(type="ShaderNodeGroup")
    view_center = node_tree.view_center
    node.location = (view_center[0] / 2.5, view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
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

class POMSTER_AddPOMsterBasic(bpy.types.Operator):
    bl_description = "Add POMster UV node"
    bl_idname = "pomster.create_basic_pom_uv"
    bl_label = "Basic POMster"
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
        create_pom_basic_nodes(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_util_ortho_tangents(node_tree):
    offset = (node_tree.view_center[0]/2.5, node_tree.view_center[1]/2.5)

    # initialize
    new_nodes = {}
    tree_nodes = node_tree.nodes

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Tangent V"
    node.location = (180+offset[0], -200+offset[1])
    node.operation = "CROSS_PRODUCT"
    node.inputs[1].default_value = (1.0, 0.0, 0.0)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Tangent U"
    node.location = (180+offset[0], 0+offset[1])
    node.operation = "CROSS_PRODUCT"
    node.inputs[1].default_value = (0.0, -1.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (0+offset[0], 0+offset[1])
    new_nodes["Geometry"] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math.001"].inputs[0])

class POMSTER_AddPOMsterUtilOrthoTangents(bpy.types.Operator):
    bl_description = "Add nodes to get U and V tangents based on XY orthographic texture projection. Use this to " \
        "get procedural U and V tangents, e.g. landscape / terrain"
    bl_idname = "pomster.create_util_orthographic_tangents"
    bl_label = "XY Orthographic Tangents"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Orthographic Tangent nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_util_ortho_tangents(context.space_data.edit_tree)
        return {'FINISHED'}
