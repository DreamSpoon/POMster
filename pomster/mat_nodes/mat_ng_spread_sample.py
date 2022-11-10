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

SPREAD_SAMPLE_MAT_NG_NAME_START = "SpreadSample"

def create_mat_ng_spread_sample(sample_num):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=
        SPREAD_SAMPLE_MAT_NG_NAME_START+str(sample_num)+ALL_MAT_NG_NAME_END, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Center")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Radius")
    for c in range(sample_num):
        new_node_group.outputs.new(type='NodeSocketFloat', name="Sample "+str(c+1))

    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-580, -40)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (60, -40)
    new_nodes["Group Output"] = node

    tree_links = new_node_group.links
    for ns in range(sample_num):
        radius_mult = 1.0 - 2 * ns / (sample_num-1)
        # do not create node if at center, but do create the link to output
        if radius_mult == 0:
            tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group Output"].inputs[ns])
            continue

        # create node
        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-240, 180-ns*200)
        node.operation = "MULTIPLY_ADD"
        node.use_clamp = False
        node.inputs[0].default_value = radius_mult

        # create links
        tree_links.new(new_nodes["Group Input"].outputs[0], node.inputs[2])
        tree_links.new(new_nodes["Group Input"].outputs[1], node.inputs[1])
        tree_links.new(node.outputs[0], new_nodes["Group Output"].inputs[ns])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
