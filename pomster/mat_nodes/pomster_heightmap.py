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

from .node_other import (ensure_node_groups, ALL_MAT_NG_NAME_END)
from .mat_ng_pomster import (create_mat_ng_pomster, POMSTER_UV_MAT_NG_NAME)
from .mat_ng_sharpen_pom import (create_mat_ng_sharpen_pom, SHARPEN_POM_MAT_NG_NAME)
from .mat_ng_spread_sample import (create_mat_ng_spread_sample, SPREAD_SAMPLE_MAT_NG_NAME_START)
from .mat_ng_error_sign_bias import (create_mat_ng_error_sign_bias, ERROR_SIGN_BIAS_MAT_NG_NAME_START)
from .mat_ng_error_cutoff import (create_mat_ng_error_cutoff, ERROR_CUTOFF_MAT_NG_NAME_START)
from .mat_ng_height_cutoff import (create_mat_ng_height_cutoff, HEIGHT_CUTOFF_MAT_NG_NAME_START)
from .mat_ng_combine_samples import (create_mat_ng_combine_samples, COMBINE_SAMPLE_MAT_NG_NAME_START)

# node names
HEIGHTMAP_ORIGINAL_NODENAME = "Heightmap.Original"
HEIGHTMAP_FINAL_NODENAME = "Heightmap.Final"

TEXTURE_COORD_INPUT_NODENAME = "UV_TextureCoordinateInput"
ASPECT_RATIO_INPUT_NODENAME = "AspectRatioInput"
TANGENT_U_INPUT_NODENAME = "TangentU_MapInput"
TANGENT_V_INPUT_NODENAME = "TangentV_MapInput"
GEOMETRY_INPUT_NODENAME = "GeometryInput"
SAMPLE_CENTER_INPUT_NODENAME = "SampleCenterInput"
SAMPLE_RADIUS_INPUT_NODENAME = "SampleRadiusInput"
HIGH_BIAS_FACTOR_INPUT_NODENAME = "HighBiasFactorInput"
SHARPEN_FACTOR_INPUT_NODENAME = "SharpenFactorInput"

# reroute node names
UV_TEX_COORD_INPUT_RR_NAME = "UV_TextureCoordinateInputReroute"
ASPECT_RATIO_INPUT_RR_NAME = "AspectRatioInputReroute"
TANGENT_U_INPUT_RR_NAME = "TangentU_InputReroute"
TANGENT_V_INPUT_RR_NAME = "TangentV_InputReroute"
GEOMETRY_NORMAL_INPUT_RR_NAME = "GeometryNormalInputReroute"
GEOMETRY_INCOMING_INPUT_RR_NAME = "GeometryIncomingInputReroute"
HIGH_BIAS_FACTOR_INPUT_RR_NAME = "HighBiasFactorInputReroute"
SHARPEN_FACTOR_INPUT_RR_NAME = "SharpenFactorInputReroute"
SAMPLE_CENTER_INPUT_RR_NAME = "SampleCenterInputReroute"
SAMPLE_RADIUS_INPUT_RR_NAME = "SampleRadiusInputReroute"

# node names
COMBINED_SAMPLE_NODENAME = "CombinedSamplePOM"

# dynamic node names
SHARPEN_POM_DYN_NODENAME = "SharpenPOM"
SHARPEN_HEIGHTMAP_DYN_NODENAME = "SharpenHeightmap"
SAMPLE_HEIGHTMAP_DYN_NODENAME = "SampleHeightmap"
SAMPLE_POM_DYN_NODENAME = "SamplePOM"
SPREAD_SAMPLE_DYN_NODENAME = "SpreadSample"
ERROR_SIGN_BIAS_DYN_NODENAME = "ErrorSignBias"
ERROR_CUTOFF_DYN_NODENAME = "ErrorCutoff"
HEIGHT_CUTOFF_DYN_NODENAME = "HeightCutoff"
COMBINE_SAMPLES_DYN_NODENAME = "CombineSamples"

def create_prereq_util_node_group(node_group_name, node_tree_type, custom_data):
    dyn_end_name = str(custom_data)+ALL_MAT_NG_NAME_END
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == POMSTER_UV_MAT_NG_NAME:
            return create_mat_ng_pomster()
        elif node_group_name == SPREAD_SAMPLE_MAT_NG_NAME_START+dyn_end_name:
            return create_mat_ng_spread_sample(custom_data)
        elif node_group_name == ERROR_SIGN_BIAS_MAT_NG_NAME_START+dyn_end_name:
            return create_mat_ng_error_sign_bias(custom_data)
        elif node_group_name == ERROR_CUTOFF_MAT_NG_NAME_START+dyn_end_name:
            return create_mat_ng_error_cutoff(custom_data)
        elif node_group_name == HEIGHT_CUTOFF_MAT_NG_NAME_START+dyn_end_name:
            return create_mat_ng_height_cutoff(custom_data)
        elif node_group_name == COMBINE_SAMPLE_MAT_NG_NAME_START+dyn_end_name:
            return create_mat_ng_combine_samples(custom_data)
        elif node_group_name == SHARPEN_POM_MAT_NG_NAME:
            return create_mat_ng_sharpen_pom()

    # error
    print("Unknown name passed to create_prereq_util_node_group: " + str(node_group_name))
    return None

def create_inputs_column(tree_nodes, tree_links, new_nodes, node_sub_offset, user_heightmap_node, user_input_index):
    separate_new_nodes = {}

    # use Texture Coordinate input node if no input UV coordinates are available
    if len(user_heightmap_node.inputs[user_input_index].links) < 1:
        node = tree_nodes.new(type="ShaderNodeTexCoord")
        node.location = (-1910+node_sub_offset, 260)
        node.from_instancer = False
        separate_new_nodes[TEXTURE_COORD_INPUT_NODENAME] = node
        input_uv_link_socket = node.outputs[2]
    # otherwise use the current input socket of UV coordinates
    else:
        input_uv_link_socket = user_heightmap_node.inputs[user_input_index].links[0].from_socket

    for i in range(len(user_heightmap_node.inputs)):
        node_input = user_heightmap_node.inputs[i]
        # if this is not the user's UV input (which gets a different reroute) and the input is linked then create
        # reroute between from and to sockets
        if i != user_input_index and len(node_input.links) > 0:
            input_link = node_input.links[0]
            from_socket = input_link.from_socket
            to_socket = input_link.to_socket

            node = tree_nodes.new(type="NodeReroute")
            node.location = (-1990+node_sub_offset, -20 * i)
            new_nodes["In_RR"+str(i)] = node

            tree_links.remove(input_link)
            tree_links.new(from_socket, node.inputs[0])
            tree_links.new(node.outputs[0], to_socket)

    # copy data needed to re-create output links, and remove links from user selected node
    output_to_sockets = []
    for node_output in user_heightmap_node.outputs:
        socks = [link.to_socket for link in node_output.links]
        output_to_sockets.append(socks)
        # remove output links
        for output_link in node_output.links:
            tree_links.remove(output_link)

    # create nodes
    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = ASPECT_RATIO_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, 0)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 1.000000
    separate_new_nodes[ASPECT_RATIO_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = TANGENT_U_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, -140)
    node.direction_type = "UV_MAP"
    separate_new_nodes[TANGENT_U_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = TANGENT_V_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, -240)
    node.direction_type = "UV_MAP"
    separate_new_nodes[TANGENT_V_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (-1910+node_sub_offset, -340)
    separate_new_nodes[GEOMETRY_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = SAMPLE_CENTER_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, -600)
    node.outputs[0].default_value = -.05
    separate_new_nodes[SAMPLE_CENTER_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = SAMPLE_RADIUS_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, -700)
    node.outputs[0].default_value = .05
    separate_new_nodes[SAMPLE_RADIUS_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = HIGH_BIAS_FACTOR_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, -800)
    node.outputs[0].default_value = 1.000000
    separate_new_nodes[HIGH_BIAS_FACTOR_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = SHARPEN_FACTOR_INPUT_NODENAME
    node.location = (-1910+node_sub_offset, -900)
    node.outputs[0].default_value = 0.500000
    separate_new_nodes[SHARPEN_FACTOR_INPUT_NODENAME] = node

    # create reroute nodes
    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, 160)
    new_nodes[UV_TEX_COORD_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -40)
    new_nodes[ASPECT_RATIO_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -180)
    new_nodes[TANGENT_U_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -280)
    new_nodes[TANGENT_V_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -400)
    new_nodes[GEOMETRY_NORMAL_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -480)
    new_nodes[GEOMETRY_INCOMING_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -640)
    new_nodes[SAMPLE_CENTER_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -740)
    new_nodes[SAMPLE_RADIUS_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -820)
    new_nodes[HIGH_BIAS_FACTOR_INPUT_RR_NAME] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-1730+node_sub_offset, -920)
    new_nodes[SHARPEN_FACTOR_INPUT_RR_NAME] = node

    # create links to reroutes
    tree_links.new(input_uv_link_socket, new_nodes[UV_TEX_COORD_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[ASPECT_RATIO_INPUT_NODENAME].outputs[0], new_nodes[ASPECT_RATIO_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[GEOMETRY_INPUT_NODENAME].outputs[1], new_nodes[GEOMETRY_NORMAL_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[GEOMETRY_INPUT_NODENAME].outputs[4], new_nodes[GEOMETRY_INCOMING_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[TANGENT_U_INPUT_NODENAME].outputs[0], new_nodes[TANGENT_U_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[TANGENT_V_INPUT_NODENAME].outputs[0], new_nodes[TANGENT_V_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[SAMPLE_CENTER_INPUT_NODENAME].outputs[0],
                   new_nodes[SAMPLE_CENTER_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[SAMPLE_RADIUS_INPUT_NODENAME].outputs[0],
                   new_nodes[SAMPLE_RADIUS_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[HIGH_BIAS_FACTOR_INPUT_NODENAME].outputs[0],
                   new_nodes[HIGH_BIAS_FACTOR_INPUT_RR_NAME].inputs[0])
    tree_links.new(separate_new_nodes[SHARPEN_FACTOR_INPUT_NODENAME].outputs[0],
                   new_nodes[SHARPEN_FACTOR_INPUT_RR_NAME].inputs[0])

    return output_to_sockets

def create_spread_sample_nodes_column(tree_nodes, tree_links, new_nodes, node_sub_offset, user_heightmap_node,
                                      user_input_index, sample_num):
    # create nodes
    for sn in range(sample_num):
        if sn == 0:
            node = user_heightmap_node
        else:
            node = duplicate_user_node(tree_nodes, user_heightmap_node)
        name_sample_heightmap_node = SAMPLE_HEIGHTMAP_DYN_NODENAME + str(sn)
        node.label = name_sample_heightmap_node
        node.location = (-1650+node_sub_offset, 240-sn*(280+user_heightmap_node.height))
        new_nodes[name_sample_heightmap_node] = node
    
        name_sample_pom_node = SAMPLE_POM_DYN_NODENAME + str(sn)
        node = tree_nodes.new(type="ShaderNodeGroup")
        node.label = name_sample_pom_node
        node.location = (-1650+node_sub_offset, 120-sn*(280+user_heightmap_node.height))
        node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
        new_nodes[name_sample_pom_node] = node

    name_spread_sample_node = SPREAD_SAMPLE_DYN_NODENAME+str(sample_num)
    name_spread_sample_group = SPREAD_SAMPLE_MAT_NG_NAME_START+str(sample_num)+ALL_MAT_NG_NAME_END
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = name_spread_sample_node
    node.location = (-1650+node_sub_offset, -130-(sample_num-1)*(280+user_heightmap_node.height))
    node.node_tree = bpy.data.node_groups.get(name_spread_sample_group)
    node.inputs[0].default_value = -0.050000
    node.inputs[1].default_value = 0.050000
    new_nodes[name_spread_sample_node] = node

    # create links
    for c in range(sample_num):
        name_sample_pom_node = SAMPLE_POM_DYN_NODENAME+str(c)
        name_sample_heightmap_node = SAMPLE_HEIGHTMAP_DYN_NODENAME+str(c)
        tree_links.new(new_nodes[name_spread_sample_node].outputs[c],
                       new_nodes[name_sample_pom_node].inputs[6])
        tree_links.new(new_nodes[name_sample_pom_node].outputs[0],
                       new_nodes[name_sample_heightmap_node].inputs[user_input_index])

def create_bcc_row(tree_nodes, tree_links, new_nodes, node_sub_offset, sample_num, error_cutoff_cycles):
    name_error_sign_bias = ERROR_SIGN_BIAS_DYN_NODENAME + str(sample_num)
#    name_error_cutoff_node = ERROR_CUTOFF_DYN_NODENAME + str(sample_num)
    name_height_cutoff_node = HEIGHT_CUTOFF_DYN_NODENAME + str(sample_num)
    name_combine_samples_node = COMBINE_SAMPLES_DYN_NODENAME + str(sample_num)

    dyn_name_end = str(sample_num)+ALL_MAT_NG_NAME_END

    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = name_error_sign_bias
    node.location = (-1390 + node_sub_offset - 200 * (error_cutoff_cycles - 1), 0)
    node.node_tree = bpy.data.node_groups.get(ERROR_SIGN_BIAS_MAT_NG_NAME_START+dyn_name_end)
    new_nodes[name_error_sign_bias] = node

    for c in range(error_cutoff_cycles):
        node = tree_nodes.new(type="ShaderNodeGroup")
        node.location = (-1190 + node_sub_offset - 200 * (error_cutoff_cycles - 1 - c), 0)
        node.node_tree = bpy.data.node_groups.get(ERROR_CUTOFF_MAT_NG_NAME_START+dyn_name_end)
        # first cycle gets init values (1, 1, 1) 
        if c == 0:
            node.inputs[1].default_value = 1.000000
            node.inputs[3].default_value = 1.000000
            node.inputs[5].default_value = 1.000000
        new_nodes[ERROR_CUTOFF_DYN_NODENAME+str(c+1)] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = name_height_cutoff_node
    node.location = (-990 + node_sub_offset, 0)
    node.node_tree = bpy.data.node_groups.get(HEIGHT_CUTOFF_MAT_NG_NAME_START+dyn_name_end)
    new_nodes[name_height_cutoff_node] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = name_combine_samples_node
    node.location = (-790 + node_sub_offset, 0)
    node.node_tree = bpy.data.node_groups.get(COMBINE_SAMPLE_MAT_NG_NAME_START+dyn_name_end)
    new_nodes[name_combine_samples_node] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = COMBINED_SAMPLE_NODENAME
    node.location = (-610 + node_sub_offset, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes[COMBINED_SAMPLE_NODENAME] = node

    # create input links to first node and output links from last node
    for sn in range(sample_num):
        tree_links.new(new_nodes[ERROR_CUTOFF_DYN_NODENAME+str(error_cutoff_cycles)].outputs[sn],
                       new_nodes[name_height_cutoff_node].inputs[1+sn*2])
        tree_links.new(new_nodes[name_height_cutoff_node].outputs[sn],
                       new_nodes[name_combine_samples_node].inputs[2+sn*3])
    # create links from error bias node to multiple (if needed) error cutoff nodes, and create links between nodes also
    for c in range(error_cutoff_cycles):
        for sn in range(sample_num):
            tree_links.new(new_nodes[name_error_sign_bias].outputs[sn],
                           new_nodes[ERROR_CUTOFF_DYN_NODENAME+str(c+1)].inputs[sn*2])
        # if this is not the first error cutoff node, then link backwards to previous error cutoff node
        if c > 0:
            # link error cutoff values from previous node to this node
            for sn in range(sample_num):
                tree_links.new(new_nodes[ERROR_CUTOFF_DYN_NODENAME+str(c)].outputs[sn],
                               new_nodes[ERROR_CUTOFF_DYN_NODENAME+str(c+1)].inputs[1+sn*2])

    tree_links.new(new_nodes[name_combine_samples_node].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[6])

def create_sharpen_pom_row(tree_nodes, tree_links, new_nodes, user_heightmap_node, sharpen_cycles):
    for c in range(sharpen_cycles):
        # create nodes
        node = duplicate_user_node(tree_nodes, user_heightmap_node)
        node.location = (-420 - 400 * (sharpen_cycles - c - 1), 0)
        new_nodes[SHARPEN_HEIGHTMAP_DYN_NODENAME+str(c+1)] = node

        node = tree_nodes.new(type="ShaderNodeGroup")
        node.location = (-200 - 400 * (sharpen_cycles - c - 1), 0)
        node.node_tree = bpy.data.node_groups.get(SHARPEN_POM_MAT_NG_NAME)
        new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)] = node

        # create links
        tree_links.new(new_nodes[SHARPEN_HEIGHTMAP_DYN_NODENAME+str(c+1)].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[7])
        # if this is not the first sharpen cycle, then get inputs from the previous sharpen cycle
        if c > 0:
            tree_links.new(new_nodes[SHARPEN_POM_DYN_NODENAME+str(c)].outputs[0],
                           new_nodes[SHARPEN_HEIGHTMAP_DYN_NODENAME+str(c+1)].inputs[0])
            tree_links.new(new_nodes[SHARPEN_POM_DYN_NODENAME+str(c)].outputs[1],
                           new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[8])

def create_pomster_apply_nodes(tree_nodes, tree_links, user_heightmap_node, user_input_index, user_output_index,
                               sample_num, error_cutoff_cycles, sharpen_cycles, enclose_nicely):
    # initialize variables
    new_nodes = {}

    node_final_offset = (user_heightmap_node.location[0], user_heightmap_node.location[1])
    node_sub_offset = -200 * (error_cutoff_cycles - 1) - 400 * (sharpen_cycles - 1)

    # create inputs column
    output_to_sockets = create_inputs_column(tree_nodes, tree_links, new_nodes, node_sub_offset, user_heightmap_node,
                                             user_input_index)
    # create spread sample column and link it to the inputs column
    create_spread_sample_nodes_column(tree_nodes, tree_links, new_nodes, node_sub_offset, user_heightmap_node,
                                      user_input_index, sample_num)
    link_input_column_to_sample_column(tree_links, new_nodes, sample_num)

    node_sub_offset = -400 * (sharpen_cycles - 1)

    # create (Bias, Cutoff, Combine) row and links
    create_bcc_row(tree_nodes, tree_links, new_nodes, node_sub_offset, sample_num, error_cutoff_cycles)
    link_input_column_to_bcc_row(tree_links, new_nodes, sample_num)
    link_sample_column_to_bcc_row(tree_links, new_nodes, sample_num)

    # create sharpen row and links
    create_sharpen_pom_row(tree_nodes, tree_links, new_nodes, user_heightmap_node, sharpen_cycles)
    link_input_column_to_sharpen_row(tree_links, new_nodes, sharpen_cycles)
    link_bcc_row_to_sharpen_row(tree_links, new_nodes, sample_num)

    # create final node, a duplicate that appears to be in the same place as the originally selected node
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.label = HEIGHTMAP_FINAL_NODENAME
    node.location = (0, 0)
    new_nodes[HEIGHTMAP_FINAL_NODENAME] = node

    # fix output links to re-create original user node's output links, but use calculated height
    relink_final_user_node(tree_nodes, tree_links, new_nodes, output_to_sockets, user_input_index, sharpen_cycles)

    # deselect all nodes in the node tree
    for n in tree_nodes.values(): n.select = False
    # select and offset all new nodes
    for n in new_nodes.values():
        n.select = True
        n.location[0] = n.location[0] + node_final_offset[0]
        n.location[1] = n.location[1] + node_final_offset[1]

    # enclose the whole setup, except for some of the input nodes (so that input links will be created correctly) 
    if enclose_nicely:
        new_nodes[HEIGHTMAP_FINAL_NODENAME].select = False
        bpy.ops.node.group_make()

    return new_nodes

def link_input_column_to_sample_column(tree_links, new_nodes, sample_num):
    name_spread_sample = SPREAD_SAMPLE_DYN_NODENAME+str(sample_num)
    # create links
    tree_links.new(new_nodes[SAMPLE_CENTER_INPUT_RR_NAME].outputs[0], new_nodes[name_spread_sample].inputs[0])
    tree_links.new(new_nodes[SAMPLE_RADIUS_INPUT_RR_NAME].outputs[0], new_nodes[name_spread_sample].inputs[1])
    for c in range(sample_num):
        name_sample_pom = SAMPLE_POM_DYN_NODENAME+str(c)
        tree_links.new(new_nodes[UV_TEX_COORD_INPUT_RR_NAME].outputs[0], new_nodes[name_sample_pom].inputs[0])
        tree_links.new(new_nodes[ASPECT_RATIO_INPUT_RR_NAME].outputs[0], new_nodes[name_sample_pom].inputs[1])
        tree_links.new(new_nodes[TANGENT_U_INPUT_RR_NAME].outputs[0], new_nodes[name_sample_pom].inputs[2])
        tree_links.new(new_nodes[TANGENT_V_INPUT_RR_NAME].outputs[0], new_nodes[name_sample_pom].inputs[3])
        tree_links.new(new_nodes[GEOMETRY_NORMAL_INPUT_RR_NAME].outputs[0], new_nodes[name_sample_pom].inputs[4])
        tree_links.new(new_nodes[GEOMETRY_INCOMING_INPUT_RR_NAME].outputs[0], new_nodes[name_sample_pom].inputs[5])

# bcc = Bias Cutoff Combine
def link_input_column_to_bcc_row(tree_links, new_nodes, sample_num):
    name_error_sign_bias = ERROR_SIGN_BIAS_DYN_NODENAME + str(sample_num)
    # create links
    tree_links.new(new_nodes[HIGH_BIAS_FACTOR_INPUT_RR_NAME].outputs[0], new_nodes[name_error_sign_bias].inputs[0])
    tree_links.new(new_nodes[UV_TEX_COORD_INPUT_RR_NAME].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[0])
    tree_links.new(new_nodes[ASPECT_RATIO_INPUT_RR_NAME].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[1])
    tree_links.new(new_nodes[TANGENT_U_INPUT_RR_NAME].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[2])
    tree_links.new(new_nodes[TANGENT_V_INPUT_RR_NAME].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[3])
    tree_links.new(new_nodes[GEOMETRY_NORMAL_INPUT_RR_NAME].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[4])
    tree_links.new(new_nodes[GEOMETRY_INCOMING_INPUT_RR_NAME].outputs[0], new_nodes[COMBINED_SAMPLE_NODENAME].inputs[5])

def link_sample_column_to_bcc_row(tree_links, new_nodes, sample_num):
    name_error_sign_bias = ERROR_SIGN_BIAS_DYN_NODENAME + str(sample_num)
    name_spread_sample = SPREAD_SAMPLE_DYN_NODENAME + str(sample_num)
    name_height_cutoff_node = HEIGHT_CUTOFF_DYN_NODENAME + str(sample_num)
    name_combine_samples_node = COMBINE_SAMPLES_DYN_NODENAME + str(sample_num)

    # create links
    for c in range(sample_num):
        name_sample_heightmap_node = SAMPLE_HEIGHTMAP_DYN_NODENAME+str(c)
        tree_links.new(new_nodes[name_sample_heightmap_node].outputs[0], new_nodes[name_error_sign_bias].inputs[1+c*2])
        tree_links.new(new_nodes[name_spread_sample].outputs[c], new_nodes[name_error_sign_bias].inputs[2+c*2])
        tree_links.new(new_nodes[name_sample_heightmap_node].outputs[0], new_nodes[name_combine_samples_node].inputs[c*3])
        tree_links.new(new_nodes[name_spread_sample].outputs[c], new_nodes[name_combine_samples_node].inputs[1+c*3])
        tree_links.new(new_nodes[name_sample_heightmap_node].outputs[0], new_nodes[name_height_cutoff_node].inputs[c*2])

def link_input_column_to_sharpen_row(tree_links, new_nodes, sharpen_cycles):
    # create links
    for c in range(sharpen_cycles):
        tree_links.new(new_nodes[UV_TEX_COORD_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[0])
        tree_links.new(new_nodes[ASPECT_RATIO_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[1])
        tree_links.new(new_nodes[TANGENT_U_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[2])
        tree_links.new(new_nodes[TANGENT_V_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[3])
        tree_links.new(new_nodes[GEOMETRY_NORMAL_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[4])
        tree_links.new(new_nodes[GEOMETRY_INCOMING_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[5])
        tree_links.new(new_nodes[SHARPEN_FACTOR_INPUT_RR_NAME].outputs[0],
                       new_nodes[SHARPEN_POM_DYN_NODENAME+str(c+1)].inputs[6])

def link_bcc_row_to_sharpen_row(tree_links, new_nodes, sample_num):
    name_combine_samples_node = COMBINE_SAMPLES_DYN_NODENAME + str(sample_num)
    tree_links.new(new_nodes[name_combine_samples_node].outputs[0],
                   new_nodes[SHARPEN_POM_DYN_NODENAME+"1"].inputs[8])
    tree_links.new(new_nodes[COMBINED_SAMPLE_NODENAME].outputs[0],
                   new_nodes[SHARPEN_HEIGHTMAP_DYN_NODENAME+"1"].inputs[0])

def duplicate_user_node(tree_nodes, user_heightmap_node):
    # de-select all nodes, ...
    for node in tree_nodes:
        node.select = False
    # except user node
    user_heightmap_node.select = True
    # duplicate only user node, keeping inputs
    bpy.ops.node.duplicate(keep_inputs=True)
    # duplicate will un-select old node, and select only the new node, so find the only node selected and return it
    for node in tree_nodes:
        if node.select:
            return node
    # return error
    return None

def relink_final_user_node(tree_nodes, tree_links, new_nodes, output_to_sockets, user_input_index, sharpen_cycles):
    tree_links.new(new_nodes[SHARPEN_POM_DYN_NODENAME+str(sharpen_cycles)].outputs[0],
                   new_nodes[HEIGHTMAP_FINAL_NODENAME].inputs[user_input_index])
    heightmap_node_loc = new_nodes[HEIGHTMAP_FINAL_NODENAME].location
    # loop through outputs
    for c in range(len(output_to_sockets)):
        # if this output had no links then skip it
        if len(output_to_sockets[c]) < 1:
            continue
        # create reroute
        node = tree_nodes.new(type="NodeReroute")
        node.location = (heightmap_node_loc[0]+200, heightmap_node_loc[1] - 20 - c * 20)
        new_nodes["Out_RR"+str(c)] = node
        # link final heightmap output to reroute
        tree_links.new(new_nodes[HEIGHTMAP_FINAL_NODENAME].outputs[c], node.inputs[0])
        # loop through connected sockets (links to other nodes) of current output, linking current reroute to other
        # node sockets
        for sock in output_to_sockets[c]:
            tree_links.new(node.outputs[0], sock)

def create_external_pomster_nodes(node_tree, override_create, user_heightmap_node, user_input_index, user_output_index,
                                sample_num, error_cutoff_cycles, sharpen_cycles, enclose_nicely):
    dyn_end_name = str(sample_num)+ALL_MAT_NG_NAME_END
    ensure_node_groups(override_create,
                       [ POMSTER_UV_MAT_NG_NAME,
                         SPREAD_SAMPLE_MAT_NG_NAME_START+dyn_end_name,
                         ERROR_SIGN_BIAS_MAT_NG_NAME_START+dyn_end_name,
                         ERROR_CUTOFF_MAT_NG_NAME_START+dyn_end_name,
                         HEIGHT_CUTOFF_MAT_NG_NAME_START+dyn_end_name,
                         COMBINE_SAMPLE_MAT_NG_NAME_START+dyn_end_name,
                         SHARPEN_POM_MAT_NG_NAME,
                        ],
                       'ShaderNodeTree', create_prereq_util_node_group, sample_num)

    create_pomster_apply_nodes(node_tree.nodes, node_tree.links, user_heightmap_node, user_input_index,
                               user_output_index, sample_num, error_cutoff_cycles, sharpen_cycles, enclose_nicely)

class POMSTER_AddPOMsterToSelectedNode(bpy.types.Operator):
    bl_description = "Using selected heightmap node as a basis, add nodes to create a Parallax Occlusion Map (POM) " \
        "effect to the material. Selected node must have at least one vector input and at least one value output"
    bl_idname = "pomster.create_heightmap_pom_uv"
    bl_label = "Heightmap POMster"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Parallax Occlusion Map nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        # get selected nodes, and proceed only if number of selected nodes equals 1
        sel_nodes = [n for n in context.space_data.edit_tree.nodes if n.select]
        if len(sel_nodes) != 1:
            self.report({'ERROR'}, "Unable to create Parallax Occlusion Map nodes because more than one Shader Node " +
                        "is selected in the editor.")
            return {'CANCELLED'}
        # check user selected node to ensure minimum amount of inputs
        user_node = sel_nodes[0]
        if len(user_node.inputs) < scn.POMSTER_UV_InputIndex:
            self.report({'ERROR'}, "Unable to create Parallax Occlusion Map nodes because selected heightmap node " +
                        "does not have enough inputs to get input number " + str(scn.POMSTER_UV_InputIndex) + " .")
            return {'CANCELLED'}
        # check user selected node to ensure minimum amount of outputs
        if len(user_node.inputs) < scn.POMSTER_HeightOutputIndex:
            self.report({'ERROR'}, "Unable to create Parallax Occlusion Map nodes because selected heightmap node " +
                        "does not have enough outputs to get output number " +
                        str(scn.POMSTER_HeightOutputIndex) + " .")
            return {'CANCELLED'}
        # check user selected node to ensure correct type of inputs
        if not hasattr(user_node.inputs[scn.POMSTER_UV_InputIndex-1], 'default_value') or \
            not hasattr(user_node.inputs[scn.POMSTER_UV_InputIndex-1].default_value, '__len__') or \
            len(user_node.inputs[scn.POMSTER_UV_InputIndex-1].default_value) != 3 or \
            not isinstance(user_node.inputs[scn.POMSTER_UV_InputIndex-1].default_value[0], float): 
            self.report({'ERROR'}, "Unable to create Parallax Occlusion Map nodes because selected heightmap node's " +
                        "input number " + str(scn.POMSTER_UV_InputIndex) + " is not a Vector type.")
            return {'CANCELLED'}
        # create the heightmap node setup in the current editor tree, with user_node as heightmap node
        create_external_pomster_nodes(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate, user_node,
                                      scn.POMSTER_UV_InputIndex-1, scn.POMSTER_HeightOutputIndex-1,
                                      scn.POMSTER_NumSamples, scn.POMSTER_NumErrorCutoffCycles,
                                      scn.POMSTER_NumSharpenCycles, scn.POMSTER_EncloseNicely)
        return {'FINISHED'}
