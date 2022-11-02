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

from .node_other import ensure_node_groups

POM_UV_MAT_NG_NAME = "POM_UV.POMSTER.MatNG"

JITTER3_MAT_NG_NAME = "Jitter3.POMSTER.MatNG"
JITTER_WEIGHT3_MAT_NG_NAME = "JitterWeight3.POMSTER.MatNG"

SAMPLE_WEIGHT1_MAT_NG_NAME = "SampleWeight1.POMSTER.MatNG"

def create_prereq_util_node_group(node_group_name, node_tree_type):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == POM_UV_MAT_NG_NAME:
            return create_mat_ng_parallax_uv()
        elif node_group_name == JITTER3_MAT_NG_NAME:
            return create_mat_ng_jitter3()
        elif node_group_name == JITTER_WEIGHT3_MAT_NG_NAME:
            return create_mat_ng_jitter_weight3()
        elif node_group_name == SAMPLE_WEIGHT1_MAT_NG_NAME:
            return create_mat_ng_sample_weight1()

    # error
    print("Unknown name passed to create_prereq_util_node_group: " + str(node_group_name))
    return None

def create_mat_ng_parallax_uv():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=POM_UV_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Height")
    new_node_group.inputs.new(type='NodeSocketVector', name="U Tangent")
    new_node_group.inputs.new(type='NodeSocketVector', name="V Tangent")
    new_node_group.inputs.new(type='NodeSocketVector', name="W Tangent")
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
    node.operation = "SUBTRACT"
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

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (-620, -320)
    new_nodes["Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-220, 200)
    node.inputs[2].default_value = 1.0
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-400, 200)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-920, -240)
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
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.004"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.006"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_mat_ng_jitter3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=JITTER3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Amount")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Bias")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Jitter 1")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Jitter 2")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Jitter 3")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -180)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = -0.5
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, 20)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 0.5
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-460, -40)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-20, -40)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.001"].inputs[2])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_mat_ng_jitter_weight3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=JITTER_WEIGHT3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Next 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Prev 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Next 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Prev 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Next 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Jitter Prev 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="PreWeight Bias")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Jitter Weighted Height")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Total Jitter Weight")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, 0)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, 0)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, -180)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, -180)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, -180)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, -180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, -180)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, -340)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, 180)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, 180)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, 180)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 180)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1120, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (380, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.001"].inputs[2])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_mat_ng_sample_weight1():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SAMPLE_WEIGHT1_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="PreWeight Bias")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Weighted Height 1")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Total Sample Weight")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-90, 0)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (90, 0)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-270, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (280, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.0
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (460, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-460, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (640, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.027"].inputs[1])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.024"].inputs[1])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_heightmap_apply_nodes(tree_nodes, tree_links, user_heightmap_node, user_input_index, user_output_index):
    # initialize variables
    new_nodes = {}

    node_loc_offset = (user_heightmap_node.location[0] + 860, user_heightmap_node.location[1] - 500)

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1780, 60)
    node.from_instancer = False
    new_nodes["Texture Coordinate.UV"] = node
    # use Texture Coordinate input node if no input UV coordinates are available
    if len(user_heightmap_node.inputs[user_input_index].links) < 1:
        input_uv_link_socket = node.outputs[2]
    # otherwise use the current input socket of UV coordinates
    else:
        input_uv_link_socket = user_heightmap_node.inputs[user_input_index].links[0].from_socket

    # copy data needed to re-create input links
    input_from_sockets = []
    for node_input in user_heightmap_node.inputs:
        if len(node_input.links) > 0:
            input_from_sockets.append(node_input.links[0].from_socket)
        else:
            input_from_sockets.append(None)

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
    node.label = "Aspect Ratio"
    node.location = (-1780, 500)
    node.inputs[0].default_value = 1.0
    node.inputs[1].default_value = 1.0
    node.inputs[2].default_value = 1.0
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "PreWeight Bias"
    node.location = (-1780, 360)
    node.outputs[0].default_value = 1.0
    new_nodes["PreWeightBias"] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = "U Tangent"
    node.location = (-1780, 260)
    node.direction_type = "UV_MAP"
    new_nodes["UVTangent"] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = "V Tangent"
    node.location = (-1780, 160)
    node.direction_type = "UV_MAP"
    new_nodes["VUTangent"] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-1600, 920-90)
    new_nodes["HeightmapJitter.000"] = node

    running_y_offset = -user_heightmap_node.dimensions[1] / 2.5

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1600, 900-90+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(POM_UV_MAT_NG_NAME)
    new_nodes["JitterPOM_Group.000"] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-1600, 670-90+running_y_offset)
    new_nodes["HeightmapJitter.001"] = node

    running_y_offset = running_y_offset - user_heightmap_node.dimensions[1] / 2.5

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1600, 730-90-80+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(POM_UV_MAT_NG_NAME)
    new_nodes["JitterPOM_Group.001"] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-1600, 500-90-80+running_y_offset)
    new_nodes["HeightmapJitter.002"] = node

    running_y_offset = running_y_offset - user_heightmap_node.dimensions[1] / 2.5

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1600, 560-90-160+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(POM_UV_MAT_NG_NAME)
    new_nodes["JitterPOM_Group.002"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1600, 330-90-160+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(JITTER3_MAT_NG_NAME)
    node.inputs[1].default_value = 0.01
    node.inputs[2].default_value = 0.0
    new_nodes["JitterGroup"] = node

    node = user_heightmap_node
    node.location = (-1600, 130-90-160+running_y_offset)
    new_nodes["Heightmap.Original"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1320, 500)
    node.node_tree = bpy.data.node_groups.get(POM_UV_MAT_NG_NAME)
    new_nodes["JitterPOM_CombineGroup"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1320, 280)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1320, 110)
    node.node_tree = bpy.data.node_groups.get(JITTER_WEIGHT3_MAT_NG_NAME)
    new_nodes["JitterWeightGroup"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1140, 500)
    node.node_tree = bpy.data.node_groups.get(POM_UV_MAT_NG_NAME)
    new_nodes["SamplePOM1Group"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1140, 280)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1140, 120)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1140, -40)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1140, -200)
    node.node_tree = bpy.data.node_groups.get(SAMPLE_WEIGHT1_MAT_NG_NAME)
    new_nodes["SampleWeight1Group"] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-1140, -390)
    new_nodes["HeightmapSample.000"] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-860, 500)
    new_nodes["Heightmap.Final"] = node
    final_user_node = node

    # create links
    tree_links.new(input_uv_link_socket, new_nodes["JitterPOM_Group.000"].inputs[0])
    tree_links.new(new_nodes["JitterGroup"].outputs[0], new_nodes["JitterPOM_Group.000"].inputs[2])
    tree_links.new(new_nodes["JitterGroup"].outputs[1], new_nodes["JitterPOM_Group.001"].inputs[2])
    tree_links.new(new_nodes["JitterGroup"].outputs[2], new_nodes["JitterPOM_Group.002"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["JitterPOM_Group.000"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["JitterPOM_Group.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["JitterPOM_Group.002"].inputs[1])
    tree_links.new(input_uv_link_socket, new_nodes["JitterPOM_Group.001"].inputs[0])
    tree_links.new(input_uv_link_socket, new_nodes["JitterPOM_Group.002"].inputs[0])
    tree_links.new(new_nodes["JitterPOM_Group.000"].outputs[0], new_nodes["HeightmapJitter.000"].inputs[user_input_index])
    tree_links.new(new_nodes["Heightmap.Original"].outputs[user_output_index], new_nodes["JitterGroup"].inputs[0])
    tree_links.new(new_nodes["Heightmap.Original"].outputs[user_output_index], new_nodes["JitterGroup"].inputs[1])
    tree_links.new(new_nodes["JitterPOM_Group.002"].outputs[0], new_nodes["HeightmapJitter.002"].inputs[user_input_index])
    tree_links.new(new_nodes["JitterPOM_Group.001"].outputs[0], new_nodes["HeightmapJitter.001"].inputs[user_input_index])
    tree_links.new(input_uv_link_socket, new_nodes["JitterPOM_CombineGroup"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["JitterPOM_CombineGroup"].inputs[1])
    tree_links.new(input_uv_link_socket, new_nodes["SamplePOM1Group"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["SamplePOM1Group"].inputs[1])
    tree_links.new(new_nodes["JitterPOM_CombineGroup"].outputs[0], new_nodes["HeightmapSample.000"].inputs[user_input_index])
    tree_links.new(new_nodes["UVTangent"].outputs[0], new_nodes["JitterPOM_Group.000"].inputs[3])
    tree_links.new(new_nodes["UVTangent"].outputs[0], new_nodes["JitterPOM_Group.001"].inputs[3])
    tree_links.new(new_nodes["UVTangent"].outputs[0], new_nodes["JitterPOM_Group.002"].inputs[3])
    tree_links.new(new_nodes["UVTangent"].outputs[0], new_nodes["JitterPOM_CombineGroup"].inputs[3])
    tree_links.new(new_nodes["UVTangent"].outputs[0], new_nodes["SamplePOM1Group"].inputs[3])
    tree_links.new(new_nodes["VUTangent"].outputs[0], new_nodes["JitterPOM_Group.000"].inputs[4])
    tree_links.new(new_nodes["VUTangent"].outputs[0], new_nodes["JitterPOM_Group.001"].inputs[4])
    tree_links.new(new_nodes["VUTangent"].outputs[0], new_nodes["JitterPOM_Group.002"].inputs[4])
    tree_links.new(new_nodes["VUTangent"].outputs[0], new_nodes["JitterPOM_CombineGroup"].inputs[4])
    tree_links.new(new_nodes["VUTangent"].outputs[0], new_nodes["SamplePOM1Group"].inputs[4])
    tree_links.new(new_nodes["HeightmapJitter.000"].outputs[user_output_index], new_nodes["JitterWeightGroup"].inputs[0])
    tree_links.new(new_nodes["HeightmapJitter.001"].outputs[user_output_index], new_nodes["JitterWeightGroup"].inputs[2])
    tree_links.new(new_nodes["HeightmapJitter.002"].outputs[user_output_index], new_nodes["JitterWeightGroup"].inputs[4])
    tree_links.new(new_nodes["PreWeightBias"].outputs[0], new_nodes["JitterWeightGroup"].inputs[6])
    tree_links.new(new_nodes["SampleWeight1Group"].outputs[1], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["HeightmapSample.000"].outputs[user_output_index], new_nodes["SampleWeight1Group"].inputs[0])
    tree_links.new(new_nodes["PreWeightBias"].outputs[0], new_nodes["SampleWeight1Group"].inputs[2])
    tree_links.new(new_nodes["JitterGroup"].outputs[2], new_nodes["JitterWeightGroup"].inputs[5])
    tree_links.new(new_nodes["JitterGroup"].outputs[1], new_nodes["JitterWeightGroup"].inputs[3])
    tree_links.new(new_nodes["JitterGroup"].outputs[0], new_nodes["JitterWeightGroup"].inputs[1])
    tree_links.new(new_nodes["JitterWeightGroup"].outputs[1], new_nodes["Math.015"].inputs[0])
    tree_links.new(input_uv_link_socket, new_nodes["Heightmap.Original"].inputs[user_input_index])
    tree_links.new(new_nodes["JitterWeightGroup"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["JitterWeightGroup"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["JitterPOM_CombineGroup"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["SampleWeight1Group"].inputs[1])
    tree_links.new(new_nodes["SampleWeight1Group"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["JitterWeightGroup"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["SamplePOM1Group"].inputs[2])
    tree_links.new(new_nodes["Texture Coordinate.UV"].outputs[1], new_nodes["JitterPOM_Group.000"].inputs[5])
    tree_links.new(new_nodes["Texture Coordinate.UV"].outputs[1], new_nodes["JitterPOM_Group.001"].inputs[5])
    tree_links.new(new_nodes["Texture Coordinate.UV"].outputs[1], new_nodes["JitterPOM_Group.002"].inputs[5])
    tree_links.new(new_nodes["Texture Coordinate.UV"].outputs[1], new_nodes["JitterPOM_CombineGroup"].inputs[5])
    tree_links.new(new_nodes["Texture Coordinate.UV"].outputs[1], new_nodes["SamplePOM1Group"].inputs[5])

    # fix output links to re-create original user node's output links, but use calculated height
    relink_final_user_node(tree_links, final_user_node, new_nodes["SamplePOM1Group"].outputs[0], output_to_sockets,
                           user_input_index)

    # deselect and offset all new nodes
    for n in new_nodes.values():
        n.select = False
        n.location[0] = n.location[0] + node_loc_offset[0]
        n.location[1] = n.location[1] + node_loc_offset[1]

    return new_nodes

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

def relink_final_user_node(tree_links, final_user_node, final_uv_input_socket, output_to_sockets, user_input_index):
    tree_links.new(final_uv_input_socket, final_user_node.inputs[user_input_index])
    # loop through outputs
    for c in range(len(output_to_sockets)):
        # loop through connected sockets (links to other nodes) of current output, linking current output to other
        # node sockets
        for sock in output_to_sockets[c]:
            tree_links.new(final_user_node.outputs[c], sock)

def create_uv_vu_pom_node_setup(node_tree, override_create, user_heightmap_node, user_input_index, user_output_index):
    ensure_node_groups(override_create,
                       [POM_UV_MAT_NG_NAME,
                        JITTER3_MAT_NG_NAME,
                        JITTER_WEIGHT3_MAT_NG_NAME,
                        SAMPLE_WEIGHT1_MAT_NG_NAME,
                        ],
                       'ShaderNodeTree', create_prereq_util_node_group)

    create_heightmap_apply_nodes(node_tree.nodes, node_tree.links, user_heightmap_node, user_input_index,
                                 user_output_index)

class POMSTER_CreateHeightmapParallaxTexture(bpy.types.Operator):
    bl_description = "Using selected node as a basis, add nodes to create a Parallax Occlusion Map (POM) effect to " \
        "the material. Selected node must have at least one vector input and at least one value output"
    bl_idname = "pomster.create_pom_uv"
    bl_label = "UV POM"
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
        create_uv_vu_pom_node_setup(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate, user_node,
                                    scn.POMSTER_UV_InputIndex-1, scn.POMSTER_HeightOutputIndex-1)
        return {'FINISHED'}
