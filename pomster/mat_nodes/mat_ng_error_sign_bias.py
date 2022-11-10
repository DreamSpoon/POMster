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

ERROR_SIGN_BIAS_MAT_NG_NAME_START = "ErrorSignBias"

def create_esb_row_start(tree_nodes, tree_links, new_nodes, sample_num):
    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "A"
    node.location = (-900, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["ES_Row1ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "A < 0"
    node.location = (-720, 180)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["ES_Row1ColB"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "A >= 0"
    node.location = (-540, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["ES_Row1ColC"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "(A >= 0) / 4"
    node.location = (-180, 180)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[1].default_value = sample_num
    new_nodes["ES_Row1ColE"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "A / 4 * high_bias"
    node.location = (0, 180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["ES_Row1ColF"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "A / 4 * high_bias + 1"
    node.location = (180, 180)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["ES_Row1ColG"] = node

    # create links
    tree_links.new(new_nodes["ES_Row1ColA"].outputs[0], new_nodes["ES_Row1ColB"].inputs[0])
    tree_links.new(new_nodes["ES_Row1ColB"].outputs[0], new_nodes["ES_Row1ColC"].inputs[1])
    tree_links.new(new_nodes["ES_Row1ColC"].outputs[0], new_nodes["ES_Row1ColE"].inputs[0])
    tree_links.new(new_nodes["ES_Row1ColE"].outputs[0], new_nodes["ES_Row1ColF"].inputs[0])
    tree_links.new(new_nodes["ES_Row1ColF"].outputs[0], new_nodes["ES_Row1ColG"].inputs[0])
    tree_links.new(new_nodes["ES_GroupInput"].outputs[0], new_nodes["ES_Row1ColF"].inputs[1])
    tree_links.new(new_nodes["ES_Row1ColA"].outputs[0], new_nodes["ES_GroupOutput"].inputs[0])

    return new_nodes["ES_Row1ColC"], new_nodes["ES_Row1ColG"]

def create_esb_row_iterate(tree_nodes, tree_links, new_nodes, prev_bias_add_node, prev_bias_mult_node, sample_num):
    for c in range(sample_num - 2):
        y_offset = -180 * c
        name_row_prepend = "ES_Row" + str(c+2)

        # create nodes
        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "B"
        node.location = (-900, y_offset)
        node.operation = "SUBTRACT"
        node.use_clamp = False
        new_nodes[name_row_prepend+"ColA"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "B < 0"
        node.location = (-720, y_offset)
        node.operation = "LESS_THAN"
        node.use_clamp = False
        node.inputs[1].default_value = 0.000000
        new_nodes[name_row_prepend+"ColB"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "B >= 0"
        node.location = (-540, y_offset)
        node.operation = "SUBTRACT"
        node.use_clamp = False
        node.inputs[0].default_value = 1.000000
        new_nodes[name_row_prepend+"ColC"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "(A >= 0) + (B >= 0)"
        node.location = (-360, y_offset)
        node.operation = "ADD"
        node.use_clamp = False
        new_nodes[name_row_prepend+"ColD"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "( (A >= 0) + (B >= 0) ) / 4"
        node.location = (-180, y_offset)
        node.operation = "DIVIDE"
        node.use_clamp = False
        node.inputs[1].default_value = sample_num
        new_nodes[name_row_prepend+"ColE"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "( (A >= 0) + (B >= 0) ) / 4 * high_bias"
        node.location = (0, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_row_prepend+"ColF"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "( (A >= 0) + (B >= 0) ) / 4 * high_bias + 1"
        node.location = (180, y_offset)
        node.operation = "ADD"
        node.use_clamp = False
        node.inputs[1].default_value = 1.000000
        new_nodes[name_row_prepend+"ColG"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.label = "B * ( A / 4 * high_bias + 1 )"
        node.location = (400, y_offset)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        new_nodes[name_row_prepend+"ColH"] = node

        # create links
        tree_links.new(new_nodes[name_row_prepend+"ColA"].outputs[0], new_nodes[name_row_prepend+"ColH"].inputs[1])
        tree_links.new(new_nodes[name_row_prepend+"ColA"].outputs[0], new_nodes[name_row_prepend+"ColB"].inputs[0])
        tree_links.new(new_nodes[name_row_prepend+"ColD"].outputs[0], new_nodes[name_row_prepend+"ColE"].inputs[0])
        tree_links.new(new_nodes[name_row_prepend+"ColB"].outputs[0], new_nodes[name_row_prepend+"ColC"].inputs[1])
        tree_links.new(new_nodes[name_row_prepend+"ColC"].outputs[0], new_nodes[name_row_prepend+"ColD"].inputs[1])
        tree_links.new(new_nodes[name_row_prepend+"ColE"].outputs[0], new_nodes[name_row_prepend+"ColF"].inputs[0])
        tree_links.new(new_nodes[name_row_prepend+"ColF"].outputs[0], new_nodes[name_row_prepend+"ColG"].inputs[0])
        tree_links.new(prev_bias_add_node.outputs[0], new_nodes[name_row_prepend+"ColD"].inputs[0])
        tree_links.new(prev_bias_mult_node.outputs[0], new_nodes[name_row_prepend+"ColH"].inputs[0])

        tree_links.new(new_nodes["ES_GroupInput"].outputs[0], new_nodes[name_row_prepend+"ColF"].inputs[1])

        tree_links.new(new_nodes[name_row_prepend+"ColH"].outputs[0], new_nodes["ES_GroupOutput"].inputs[c+1])

    return new_nodes[name_row_prepend+"ColG"]

def create_esb_row_end(tree_nodes, tree_links, new_nodes, row_bias_mult, row_num):
    name_row_prepend = "ES_Row" + str(row_num)

    y_offset = -180 * (row_num - 2)

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "C"
    node.location = (-900, y_offset)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes[name_row_prepend+"ColA"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "C * ( ( (A >= 0) + (B >= 0) + (X >= 0) ) / 4 * high_bias + 1 )"
    node.location = (400, y_offset)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes[name_row_prepend+"ColH"] = node

    # create links
    tree_links.new(new_nodes[name_row_prepend+"ColA"].outputs[0], new_nodes[name_row_prepend+"ColH"].inputs[1])
    tree_links.new(row_bias_mult.outputs[0], new_nodes[name_row_prepend+"ColH"].inputs[0])

    tree_links.new(new_nodes["ES_GroupInput"].outputs[1+(row_num-1)*2], new_nodes[name_row_prepend+"ColA"].inputs[0])
    tree_links.new(new_nodes["ES_GroupInput"].outputs[2+(row_num-1)*2], new_nodes[name_row_prepend+"ColA"].inputs[1])

    tree_links.new(new_nodes[name_row_prepend+"ColH"].outputs[0], new_nodes["ES_GroupOutput"].inputs[row_num-1])

def create_mat_ng_error_sign_bias(sample_num):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=
        ERROR_SIGN_BIAS_MAT_NG_NAME_START+str(sample_num)+ALL_MAT_NG_NAME_END, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="High Bias Factor")
    for sn in range(sample_num):
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next "+str(sn+1))
        new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev "+str(sn+1))
        new_node_group.outputs.new(type='NodeSocketFloat', name="Error "+str(sn+1))

    tree_nodes = new_node_group.nodes
    tree_links = new_node_group.links

    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1120, 0)
    new_nodes["ES_GroupInput"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (580, 20)
    new_nodes["ES_GroupOutput"] = node

    # create dynamic nodes and links
    prev_bias_add_node, prev_bias_mult_node = create_esb_row_start(tree_nodes, tree_links, new_nodes, sample_num)
    # TODO move this for loop into the function  create_esb_row_iterate()
#    for c in range(sample_num - 2):
#        temp_bias_add_node, temp_bias_mult_node = create_esb_row_iterate(tree_nodes, tree_links, new_nodes,
#            prev_bias_add_node, prev_bias_mult_node, sample_num, c+2)
#        prev_bias_add_node, prev_bias_mult_node = temp_bias_add_node, temp_bias_mult_node
    final_bias_mult_node = create_esb_row_iterate(tree_nodes, tree_links, new_nodes, prev_bias_add_node,
                                                  prev_bias_mult_node, sample_num)
    create_esb_row_end(tree_nodes, tree_links, new_nodes, final_bias_mult_node, sample_num)

    # create dynamic links
    tree_links.new(new_nodes["ES_GroupInput"].outputs[1], new_nodes["ES_Row1ColA"].inputs[0])
    tree_links.new(new_nodes["ES_GroupInput"].outputs[2], new_nodes["ES_Row1ColA"].inputs[1])
    #
    for c in range(sample_num-2):
        name_row_prepend = "ES_Row" + str(c+2)
        tree_links.new(new_nodes["ES_GroupInput"].outputs[3+c*2], new_nodes[name_row_prepend+"ColA"].inputs[0])
        tree_links.new(new_nodes["ES_GroupInput"].outputs[4+c*2], new_nodes[name_row_prepend+"ColA"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
