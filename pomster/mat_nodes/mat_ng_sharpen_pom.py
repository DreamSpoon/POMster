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

from .node_other import ALL_MAT_NG_NAME_END
from .mat_ng_pomster import POMSTER_UV_MAT_NG_NAME

SHARPEN_POM_MAT_NG_NAME = "SharpenPOM" + ALL_MAT_NG_NAME_END

def create_mat_ng_sharpen_pom():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SHARPEN_POM_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sharpen Factor")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Next Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Prev Height")
    new_node_group.outputs.new(type='NodeSocketVector', name="UV Output")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Height")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -340)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (0, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-360, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (190, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[2])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group"].inputs[5])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
