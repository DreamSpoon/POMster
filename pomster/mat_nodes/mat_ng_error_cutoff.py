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

ERROR_CUTOFF_MAT_NG_NAME_START = "ErrorCutoff"

def create_ec_column_add(tree_nodes, tree_links, new_nodes, sample_num, prev_add_node):
    for r in range(sample_num-2):
        name_row_prepend = "EC_Row"+str(r+2)+"ColA"

        # create node
        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (-160, -200-r*180)
        node.operation = "ADD"
        node.use_clamp = False
        new_nodes[name_row_prepend] = node

        # create links
        tree_links.new(node.outputs[0], prev_add_node.inputs[1])

        # if this is the last add node, then use the last two samples, instead of just 1
        if r == sample_num-3:
            tree_links.new(new_nodes["EC_GroupInput"].outputs[3+r*2], node.inputs[0])
            tree_links.new(new_nodes["EC_GroupInput"].outputs[5+r*2], node.inputs[1])
        # otherwise just use one
        else:
            tree_links.new(new_nodes["EC_GroupInput"].outputs[3+r*2], node.inputs[0])

        prev_add_node = node

def create_ec_row_start(tree_nodes, tree_links, new_nodes):
    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-160, 160)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["EC_Row1ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Count"
    node.location = (20, 160)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["EC_Row1ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Average Error"
    node.location = (200, 160)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["EC_Row1ColC"] = node

    # create links
    tree_links.new(new_nodes["EC_Row1ColA"].outputs[0], new_nodes["EC_Row1ColB"].inputs[0])
    tree_links.new(new_nodes["EC_Row1ColB"].outputs[0], new_nodes["EC_Row1ColC"].inputs[1])

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (640, -20)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["EC_Row2ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (460, -20)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["EC_Row2ColD"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (200, -20)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["EC_Row2ColC"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (20, -20)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["EC_Row2ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-160, -20)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["EC_Row2ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Weight 1"
    node.location = (820, -20)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["EC_Row2ColF"] = node

    # create links
    tree_links.new(new_nodes["EC_Row2ColD"].outputs[0], new_nodes["EC_Row2ColE"].inputs[1])
    tree_links.new(new_nodes["EC_Row2ColE"].outputs[0], new_nodes["EC_Row2ColF"].inputs[0])
    tree_links.new(new_nodes["EC_Row2ColB"].outputs[0], new_nodes["EC_Row2ColC"].inputs[0])

    # create links to input and output
    tree_links.new(new_nodes["EC_GroupInput"].outputs[1], new_nodes["EC_Row2ColA"].inputs[0])
    tree_links.new(new_nodes["EC_GroupInput"].outputs[0], new_nodes["EC_Row2ColB"].inputs[0])
    tree_links.new(new_nodes["EC_GroupInput"].outputs[1], new_nodes["EC_Row2ColB"].inputs[1])
    tree_links.new(new_nodes["EC_GroupInput"].outputs[0], new_nodes["EC_Row2ColD"].inputs[0])
    tree_links.new(new_nodes["EC_GroupInput"].outputs[1], new_nodes["EC_Row2ColF"].inputs[1])
    tree_links.new(new_nodes["EC_Row2ColF"].outputs[0], new_nodes["EC_GroupOutput"].inputs[0])

    # create links from this row to row1
    tree_links.new(new_nodes["EC_Row2ColC"].outputs[0], new_nodes["EC_Row1ColC"].inputs[0])
    tree_links.new(new_nodes["EC_Row1ColC"].outputs[0], new_nodes["EC_Row2ColD"].inputs[1])
    tree_links.new(new_nodes["EC_Row2ColA"].outputs[0], new_nodes["EC_Row1ColA"].inputs[0])
    tree_links.new(new_nodes["EC_Row1ColA"].outputs[0], new_nodes["EC_Row1ColB"].inputs[0])
    tree_links.new(new_nodes["EC_Row2ColA"].outputs[0], new_nodes["EC_Row1ColB"].inputs[1])
    tree_links.new(new_nodes["EC_Row1ColB"].outputs[0], new_nodes["EC_Row1ColC"].inputs[1])

    return new_nodes["EC_Row2ColA"], new_nodes["EC_Row2ColC"], new_nodes["EC_Row1ColC"]

def create_ec_row_iterate(tree_nodes, tree_links, new_nodes, prev_error_add_node, average_error_node, repeat_num):
    for r in range(repeat_num):
        y_offset = -200 - r * 160
        name_ec_row = "EC_Row" + str(3 + r)

        # create nodes
        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (20, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColB"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (200, y_offset)
        node.operation = "ADD"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColC"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (460, y_offset)
        node.operation = "GREATER_THAN"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColD"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (640, y_offset)
        node.operation = "SUBTRACT"
        node.use_clamp = False
        node.inputs[0].default_value = 1.000000
        new_nodes[name_ec_row+"ColE"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "Cutoff Sample Weight 2"
        node.location = (820, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_ec_row+"ColF"] = node

        # create links
        tree_links.new(new_nodes[name_ec_row+"ColB"].outputs[0], new_nodes[name_ec_row+"ColC"].inputs[0])
        tree_links.new(new_nodes[name_ec_row+"ColD"].outputs[0], new_nodes[name_ec_row+"ColE"].inputs[1])
        tree_links.new(new_nodes[name_ec_row+"ColE"].outputs[0], new_nodes[name_ec_row+"ColF"].inputs[0])

        tree_links.new(new_nodes["EC_GroupInput"].outputs[2+r*2], new_nodes[name_ec_row+"ColB"].inputs[0])
        tree_links.new(new_nodes["EC_GroupInput"].outputs[4+r*2], new_nodes[name_ec_row+"ColB"].inputs[1])

        tree_links.new(new_nodes[name_ec_row+"ColC"].outputs[0], prev_error_add_node.inputs[1])

        tree_links.new(average_error_node.outputs[0], new_nodes[name_ec_row+"ColD"].inputs[1])

        tree_links.new(new_nodes["EC_GroupInput"].outputs[2+r*2], new_nodes[name_ec_row+"ColD"].inputs[0])

        tree_links.new(new_nodes["EC_GroupInput"].outputs[2+r*2], new_nodes[name_ec_row+"ColF"].inputs[1])

        tree_links.new(new_nodes[name_ec_row+"ColF"].outputs[0], new_nodes["EC_GroupOutput"].inputs[1+r])

        # update previous node ref
        prev_error_add_node = new_nodes[name_ec_row+"ColC"]

    return prev_error_add_node

def create_ec_row_end(tree_nodes, tree_links, new_nodes, final_error_add_node, average_error_node, row_num):
    y_offset = -380 - (row_num - 4) * 160
    name_ec_row = "EC_Row" + str(row_num)

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Weight 3"
    node.location = (820, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_ec_row+"ColF"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (640, y_offset)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes[name_ec_row+"ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (460, y_offset)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes[name_ec_row+"ColD"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (20, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_ec_row+"ColB"] = node

    # create links
    tree_links.new(new_nodes[name_ec_row+"ColD"].outputs[0], new_nodes[name_ec_row+"ColE"].inputs[1])
    tree_links.new(new_nodes[name_ec_row+"ColE"].outputs[0], new_nodes[name_ec_row+"ColF"].inputs[0])

    tree_links.new(new_nodes[name_ec_row+"ColB"].outputs[0], final_error_add_node.inputs[1])

    tree_links.new(new_nodes["EC_GroupInput"].outputs[4+(row_num-4)*2], new_nodes[name_ec_row+"ColB"].inputs[0])
    tree_links.new(new_nodes["EC_GroupInput"].outputs[5+(row_num-4)*2], new_nodes[name_ec_row+"ColB"].inputs[1])

    tree_links.new(average_error_node.outputs[0], new_nodes[name_ec_row+"ColD"].inputs[1])

    tree_links.new(new_nodes["EC_GroupInput"].outputs[4+(row_num-4)*2], new_nodes[name_ec_row+"ColD"].inputs[0])

    tree_links.new(new_nodes["EC_GroupInput"].outputs[4+(row_num-4)*2], new_nodes[name_ec_row+"ColF"].inputs[1])

    tree_links.new(new_nodes[name_ec_row+"ColF"].outputs[0], new_nodes["EC_GroupOutput"].inputs[2+(row_num-4)])

def create_mat_ng_error_cutoff(sample_num):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=ERROR_CUTOFF_MAT_NG_NAME_START+str(sample_num)+ALL_MAT_NG_NAME_END,
                                              type='ShaderNodeTree')
    for sn in range(sample_num):
        new_node_group.inputs.new(type='NodeSocketFloat', name="Error "+str(sn+1))
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff "+str(sn+1))
        new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Cutoff "+str(sn+1))

    tree_nodes = new_node_group.nodes
    tree_links = new_node_group.links

    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-400, -20)
    new_nodes["EC_GroupInput"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1020, -20)
    new_nodes["EC_GroupOutput"] = node

    prev_cutoff_add_node, prev_error_add_node, average_error_node = create_ec_row_start(tree_nodes, tree_links,
                                                                                        new_nodes)
    create_ec_column_add(tree_nodes, tree_links, new_nodes, sample_num, prev_cutoff_add_node)
    final_error_add_node = create_ec_row_iterate(tree_nodes, tree_links, new_nodes, prev_error_add_node,
                                                 average_error_node, sample_num-2)
    create_ec_row_end(tree_nodes, tree_links, new_nodes, final_error_add_node, average_error_node, sample_num+1)

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
