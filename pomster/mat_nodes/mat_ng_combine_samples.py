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

COMBINE_SAMPLE_MAT_NG_NAME_START = "CombineSample"

def create_cs_row_start(tree_nodes, tree_links, new_nodes):
    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1980, 0)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["CS_Row2ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, 0)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["CS_Row2ColC"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1620, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["CS_Row2ColD"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1440, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["CS_Row2ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Weighted Height"
    node.location = (-1260, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["CS_Row2ColF"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Total Weight"
    node.location = (-1080, 0)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["CS_Row2ColG"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["CS_Row2ColH"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2160, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["CS_Row2ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Not Equal 0"
    node.location = (-680, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["CS_Row1ColI"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-500, 180)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["CS_Row1ColJ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Equal 0"
    node.location = (-680, 0)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["CS_Row2ColI"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-500, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["CS_Row2ColJ"] = node

    # create links
    tree_links.new(new_nodes["CS_Row2ColD"].outputs[0], new_nodes["CS_Row2ColE"].inputs[1])
    tree_links.new(new_nodes["CS_Row2ColA"].outputs[0], new_nodes["CS_Row2ColB"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColB"].outputs[0], new_nodes["CS_Row2ColC"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColE"].outputs[0], new_nodes["CS_Row2ColF"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColE"].outputs[0], new_nodes["CS_Row2ColG"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColG"].outputs[0], new_nodes["CS_Row2ColH"].inputs[1])
    tree_links.new(new_nodes["CS_Row2ColF"].outputs[0], new_nodes["CS_Row2ColH"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColC"].outputs[0], new_nodes["CS_Row2ColD"].inputs[1])
    tree_links.new(new_nodes["CS_Row2ColG"].outputs[0], new_nodes["CS_Row2ColI"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColI"].outputs[0], new_nodes["CS_Row1ColI"].inputs[1])
    tree_links.new(new_nodes["CS_Row1ColI"].outputs[0], new_nodes["CS_Row1ColJ"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColI"].outputs[0], new_nodes["CS_Row2ColJ"].inputs[0])
    tree_links.new(new_nodes["CS_Row2ColJ"].outputs[0], new_nodes["CS_Row1ColJ"].inputs[2])
    tree_links.new(new_nodes["CS_Row2ColH"].outputs[0], new_nodes["CS_Row1ColJ"].inputs[1])
    tree_links.new(new_nodes["CS_Row1ColJ"].outputs[0], new_nodes["CS_GroupOutput"].inputs[0])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[0], new_nodes["CS_Row2ColA"].inputs[0])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[1], new_nodes["CS_Row2ColA"].inputs[1])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[0], new_nodes["CS_Row2ColF"].inputs[1])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[2], new_nodes["CS_Row2ColE"].inputs[0])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[0], new_nodes["CS_Row2ColJ"].inputs[1])

    return new_nodes["CS_Row2ColF"], new_nodes["CS_Row2ColG"]

def create_cs_row_iterate(tree_nodes, tree_links, new_nodes, weighted_height_node, total_weight_node, sample_num):
    for c in range(sample_num-2):
        y_offset = -200 - c*160
        name_cs_row = "CS_Row" + str(c+3)

        # create nodes
        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-2160, y_offset)
        node.operation = "SUBTRACT"
        node.use_clamp = False
        new_nodes[name_cs_row+"ColA"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-1980, y_offset)
        node.operation = "ABSOLUTE"
        node.use_clamp = False
        new_nodes[name_cs_row+"ColB"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-1800, y_offset)
        node.operation = "ADD"
        node.use_clamp = False
        node.inputs[1].default_value = 1.000000
        new_nodes[name_cs_row+"ColC"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-1620, y_offset)
        node.operation = "DIVIDE"
        node.use_clamp = False
        node.inputs[0].default_value = 1.000000
        new_nodes[name_cs_row+"ColD"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-1440, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_cs_row+"ColE"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-1080, y_offset)
        node.operation = "ADD"
        node.use_clamp = False
        new_nodes[name_cs_row+"ColG"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-1260, y_offset)
        node.operation = "MULTIPLY_ADD"
        node.use_clamp = False
        new_nodes[name_cs_row+"ColF"] = node

        # create links
        tree_links.new(new_nodes[name_cs_row+"ColD"].outputs[0], new_nodes[name_cs_row+"ColE"].inputs[1])
        tree_links.new(new_nodes[name_cs_row+"ColB"].outputs[0], new_nodes[name_cs_row+"ColC"].inputs[0])
        tree_links.new(new_nodes[name_cs_row+"ColA"].outputs[0], new_nodes[name_cs_row+"ColB"].inputs[0])
        tree_links.new(new_nodes[name_cs_row+"ColE"].outputs[0], new_nodes[name_cs_row+"ColF"].inputs[0])
        tree_links.new(new_nodes[name_cs_row+"ColE"].outputs[0], new_nodes[name_cs_row+"ColG"].inputs[0])
        tree_links.new(new_nodes[name_cs_row+"ColC"].outputs[0], new_nodes[name_cs_row+"ColD"].inputs[1])
        tree_links.new(new_nodes["CS_GroupInput"].outputs[3+c*3], new_nodes[name_cs_row+"ColA"].inputs[0])
        tree_links.new(new_nodes["CS_GroupInput"].outputs[4+c*3], new_nodes[name_cs_row+"ColA"].inputs[1])
        tree_links.new(new_nodes["CS_GroupInput"].outputs[3+c*3], new_nodes[name_cs_row+"ColF"].inputs[1])
        tree_links.new(new_nodes["CS_GroupInput"].outputs[5+c*3], new_nodes[name_cs_row+"ColE"].inputs[0])

        tree_links.new(new_nodes[name_cs_row+"ColF"].outputs[0], weighted_height_node.inputs[2])
        tree_links.new(new_nodes[name_cs_row+"ColG"].outputs[0], total_weight_node.inputs[1])

        # update ref to previous
        weighted_height_node, total_weight_node = new_nodes[name_cs_row+"ColF"], new_nodes[name_cs_row+"ColG"]

    name_cs_row = "CS_Row" + str(sample_num)
    return new_nodes[name_cs_row+"ColF"], new_nodes[name_cs_row+"ColG"]

def create_cs_row_end(tree_nodes, tree_links, new_nodes, weighted_height_node, total_weight_node, sample_num):
    y_offset = 80 - sample_num * 160
    name_cs_row = "CS_Row" + str(sample_num+1)

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2160, y_offset)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes[name_cs_row+"ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1980, y_offset)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes[name_cs_row+"ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, y_offset)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes[name_cs_row+"ColC"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1620, y_offset)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes[name_cs_row+"ColD"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1440, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_cs_row+"ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_cs_row+"ColF"] = node

    # create links
    tree_links.new(new_nodes[name_cs_row+"ColD"].outputs[0], new_nodes[name_cs_row+"ColE"].inputs[1])
    tree_links.new(new_nodes[name_cs_row+"ColB"].outputs[0], new_nodes[name_cs_row+"ColC"].inputs[0])
    tree_links.new(new_nodes[name_cs_row+"ColA"].outputs[0], new_nodes[name_cs_row+"ColB"].inputs[0])
    tree_links.new(new_nodes[name_cs_row+"ColE"].outputs[0], new_nodes[name_cs_row+"ColF"].inputs[0])
    tree_links.new(new_nodes[name_cs_row+"ColC"].outputs[0], new_nodes[name_cs_row+"ColD"].inputs[1])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[-3+sample_num*3], new_nodes[name_cs_row+"ColA"].inputs[0])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[-2+sample_num*3], new_nodes[name_cs_row+"ColA"].inputs[1])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[-3+sample_num*3], new_nodes[name_cs_row+"ColF"].inputs[1])
    tree_links.new(new_nodes["CS_GroupInput"].outputs[-1+sample_num*3], new_nodes[name_cs_row+"ColE"].inputs[0])

    tree_links.new(new_nodes[name_cs_row+"ColF"].outputs[0], weighted_height_node.inputs[2])
    tree_links.new(new_nodes[name_cs_row+"ColE"].outputs[0], total_weight_node.inputs[1])

def create_mat_ng_combine_samples(sample_num):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=
        COMBINE_SAMPLE_MAT_NG_NAME_START+str(sample_num)+ALL_MAT_NG_NAME_END, type='ShaderNodeTree')
    for sn in range(sample_num):
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next "+str(sn+1))
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev "+str(sn+1))
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff "+str(sn+1))

    new_node_group.outputs.new(type='NodeSocketFloat', name="Height ")

    tree_nodes = new_node_group.nodes
    tree_links = new_node_group.links

    # delete all nodes
    tree_nodes.clear()

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2400, 0)
    new_nodes["CS_GroupInput"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-320, 180)
    new_nodes["CS_GroupOutput"] = node

    weighted_height_node, total_weight_node = create_cs_row_start(tree_nodes, tree_links, new_nodes)
    weighted_height_node, total_weight_node = create_cs_row_iterate(tree_nodes, tree_links, new_nodes,
        weighted_height_node, total_weight_node, sample_num)
    create_cs_row_end(tree_nodes, tree_links, new_nodes, weighted_height_node, total_weight_node, sample_num)

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
