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

HEIGHT_CUTOFF_MAT_NG_NAME_START = "HeightCutoff"

def create_hc_row_start(tree_nodes, tree_links, new_nodes):
    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Average Height"
    node.location = (280, 40)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["HC_Row1ColC"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, 40)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["HC_Row1ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Ensure > 0"
    node.location = (-80, -120)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["HC_Row2ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-80, -300)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["HC_Row3ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (100, -120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["HC_Row2ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (280, -120)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["HC_Row2ColC"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, -120)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["HC_Row2ColD"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, -120)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["HC_Row2ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Height 1"
    node.location = (900, -120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["HC_Row2ColF"] = node

    # create links
    tree_links.new(new_nodes["HC_GroupInput"].outputs[0], new_nodes["HC_Row2ColB"].inputs[0])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[1], new_nodes["HC_Row2ColB"].inputs[1])
    tree_links.new(new_nodes["HC_Row2ColF"].outputs[0], new_nodes["HC_GroupOutput"].inputs[0])
    tree_links.new(new_nodes["HC_Row2ColC"].outputs[0], new_nodes["HC_Row1ColC"].inputs[0])
    tree_links.new(new_nodes["HC_Row2ColB"].outputs[0], new_nodes["HC_Row2ColC"].inputs[0])
    tree_links.new(new_nodes["HC_Row2ColD"].outputs[0], new_nodes["HC_Row2ColE"].inputs[1])
    tree_links.new(new_nodes["HC_Row2ColE"].outputs[0], new_nodes["HC_Row2ColF"].inputs[0])
    tree_links.new(new_nodes["HC_Row1ColC"].outputs[0], new_nodes["HC_Row2ColD"].inputs[1])
    tree_links.new(new_nodes["HC_Row3ColA"].outputs[0], new_nodes["HC_Row2ColA"].inputs[0])
    tree_links.new(new_nodes["HC_Row2ColA"].outputs[0], new_nodes["HC_Row1ColA"].inputs[0])
    tree_links.new(new_nodes["HC_Row3ColA"].outputs[0], new_nodes["HC_Row1ColA"].inputs[1])
    tree_links.new(new_nodes["HC_Row1ColA"].outputs[0], new_nodes["HC_Row1ColC"].inputs[1])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[1], new_nodes["HC_Row2ColF"].inputs[1])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[0], new_nodes["HC_Row2ColD"].inputs[0])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[1], new_nodes["HC_Row3ColA"].inputs[0])

    return new_nodes["HC_Row3ColA"], new_nodes["HC_Row2ColC"], new_nodes["HC_Row1ColC"]

def create_hc_column_cutoff_add(tree_nodes, tree_links, new_nodes, cutoff_add_column_node, sample_num):
    prev_add_node = cutoff_add_column_node
    for c in range(sample_num-2):
        name_hc_row = "HC_Row" + str(c)
        # create node
        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-80, -480-c*160)
        node.operation = "ADD"
        node.use_clamp = False
        new_nodes[name_hc_row+"ColA"] = node

        # create links
        tree_links.new(node.outputs[0], prev_add_node.inputs[1])
        # if this is the last node, then connect inputs to 2 samples
        if c == sample_num - 3:
            tree_links.new(new_nodes["HC_GroupInput"].outputs[sample_num*2-3], node.inputs[0])
            tree_links.new(new_nodes["HC_GroupInput"].outputs[sample_num*2-1], node.inputs[1])
        # otherwise connect 1 input to 1 sample
        else:
            tree_links.new(new_nodes["HC_GroupInput"].outputs[c*2+3], node.inputs[0])

        # update ref to previous
        prev_add_node = node

def create_hc_row_iterate(tree_nodes, tree_links, new_nodes, height_add_column_node, average_height_node, sample_num):
    prev_add_node = height_add_column_node
    for c in range(sample_num-2):
        y_offset = -300 - c * 160
        name_ec_row = "HC_Row" + str(c+3)

        # create nodes
        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (100, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColB"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (280, y_offset)
        node.operation = "ADD"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColC"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (540, y_offset)
        node.operation = "LESS_THAN"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColD"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (720, y_offset)
        node.operation = "SUBTRACT"
        node.use_clamp = False
        node.inputs[0].default_value = 1.000000
        new_nodes[name_ec_row+"ColE"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "Cutoff Sample Height 2"
        node.location = (900, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColF"] = node

        # create links
        tree_links.new(new_nodes["HC_GroupInput"].outputs[2+c*2], new_nodes[name_ec_row+"ColB"].inputs[0])
        tree_links.new(new_nodes["HC_GroupInput"].outputs[3+c*2], new_nodes[name_ec_row+"ColB"].inputs[1])
        tree_links.new(new_nodes[name_ec_row+"ColF"].outputs[0], new_nodes["HC_GroupOutput"].inputs[1+c])
        tree_links.new(new_nodes[name_ec_row+"ColB"].outputs[0], new_nodes[name_ec_row+"ColC"].inputs[0])
        tree_links.new(new_nodes[name_ec_row+"ColD"].outputs[0], new_nodes[name_ec_row+"ColE"].inputs[1])
        tree_links.new(new_nodes[name_ec_row+"ColE"].outputs[0], new_nodes[name_ec_row+"ColF"].inputs[0])
        tree_links.new(new_nodes["HC_GroupInput"].outputs[2+c*2], new_nodes[name_ec_row+"ColD"].inputs[0])
        tree_links.new(new_nodes["HC_GroupInput"].outputs[3+c*2], new_nodes[name_ec_row+"ColF"].inputs[1])

        tree_links.new(new_nodes[name_ec_row+"ColC"].outputs[0], prev_add_node.inputs[1])
        tree_links.new(average_height_node.outputs[0], new_nodes[name_ec_row+"ColD"].inputs[1])

        prev_add_node = new_nodes[name_ec_row+"ColC"]

    return new_nodes["HC_Row"+str(sample_num)+"ColC"] 

def create_hc_row_end(tree_nodes, tree_links, new_nodes, final_height_add_node, average_height_node, sample_num):
    name_ec_row = "HC_Row" + str(sample_num+1)
    y_offset = -160 * sample_num

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (100, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_ec_row+"ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (540, y_offset)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes[name_ec_row+"ColD"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (720, y_offset)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes[name_ec_row+"ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Height 3"
    node.location = (900, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_ec_row+"ColF"] = node

    # create links
    tree_links.new(new_nodes["HC_GroupInput"].outputs[-2+sample_num*2], new_nodes[name_ec_row+"ColB"].inputs[0])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[-1+sample_num*2], new_nodes[name_ec_row+"ColB"].inputs[1])
    tree_links.new(new_nodes[name_ec_row+"ColF"].outputs[0], new_nodes["HC_GroupOutput"].inputs[sample_num-1])
    tree_links.new(new_nodes[name_ec_row+"ColD"].outputs[0], new_nodes[name_ec_row+"ColE"].inputs[1])
    tree_links.new(new_nodes[name_ec_row+"ColE"].outputs[0], new_nodes[name_ec_row+"ColF"].inputs[0])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[-2+sample_num*2], new_nodes[name_ec_row+"ColD"].inputs[0])
    tree_links.new(new_nodes["HC_GroupInput"].outputs[-1+sample_num*2], new_nodes[name_ec_row+"ColF"].inputs[1])

    tree_links.new(new_nodes[name_ec_row+"ColB"].outputs[0], final_height_add_node.inputs[1])
    tree_links.new(average_height_node.outputs[0], new_nodes[name_ec_row+"ColD"].inputs[1])

def create_mat_ng_height_cutoff(sample_num):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=HEIGHT_CUTOFF_MAT_NG_NAME_START+str(sample_num)+ALL_MAT_NG_NAME_END,
                                              type='ShaderNodeTree')
    for sn in range(sample_num):
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next "+str(sn+1))
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff "+str(sn+1))
        new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Cutoff "+str(sn+1))

    tree_nodes = new_node_group.nodes
    tree_links = new_node_group.links

    # delete all nodes
    tree_nodes.clear()

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-480, -120)
    new_nodes["HC_GroupInput"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1120, -300)
    new_nodes["HC_GroupOutput"] = node

    cutoff_add_column_node, height_add_column_node, average_height_node  = create_hc_row_start(tree_nodes, tree_links,
                                                                                               new_nodes)
    create_hc_column_cutoff_add(tree_nodes, tree_links, new_nodes, cutoff_add_column_node, sample_num)
    final_height_add_node = create_hc_row_iterate(tree_nodes, tree_links, new_nodes, height_add_column_node,
                                                  average_height_node, sample_num)
    create_hc_row_end(tree_nodes, tree_links, new_nodes, final_height_add_node, average_height_node, sample_num)

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
