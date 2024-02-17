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

import math
import bpy

from ..node_other import (get_tangent_map_name, ensure_node_group, MAT_NG_NAME_SUFFIX)
from .parallax_map import (create_mat_ng_parallax_map, PARALLAX_MAP_MAT_NG_NAME)

OFFSET_CONESTEP_POM_MAT_NG_NAME = "OffsetConestepPOM" + MAT_NG_NAME_SUFFIX
ITERATE_MAT_NG_NAME = "_iterate" + MAT_NG_NAME_SUFFIX
BLANK_NODE_GROUP_NAME = "InputOCPOM" + MAT_NG_NAME_SUFFIX

OCPOM_NODENAME = "OCPOM Node"
UV_INPUT_NODENAME = "UV Input"
TANGENT_U_INPUT_NODENAME = "Tangent U"
TANGENT_V_INPUT_NODENAME = "Tangent V"
GEOMETRY_INPUT_NODENAME = "Geometry Input"

def create_prereq_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == PARALLAX_MAP_MAT_NG_NAME:
            return create_mat_ng_parallax_map()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_mat_ng_iterate(custom_data):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=ITERATE_MAT_NG_NAME, type='ShaderNodeTree')

    # remove old group inputs and outputs
    if bpy.app.version >= (4, 0, 0):
        for item in new_node_group.interface.items_tree:
            if item.item_type == 'SOCKET':
                new_node_group.interface.remove(item)
    else:
        new_node_group.inputs.clear()
        new_node_group.outputs.clear()
    # create new group inputs and outputs
    new_in_socket = {}
    if bpy.app.version >= (4, 0, 0):
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Finished", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="UV Input", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Aspect Ratio", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Tangent U", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Tangent V", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Normal", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Incoming", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Current Height", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Current Texel Height", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Current Texel Cone Ratio", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Current Texel Cone Offset", in_out='INPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Step Height", in_out='INPUT')
    else:
        new_node_group.inputs.new(type='NodeSocketFloat', name="Finished")
        new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
        new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
        new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U")
        new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V")
        new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
        new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
        new_node_group.inputs.new(type='NodeSocketFloat', name="Current Height")
        new_node_group.inputs.new(type='NodeSocketFloat', name="Current Texel Height")
        new_node_group.inputs.new(type='NodeSocketFloat', name="Current Texel Cone Ratio")
        new_node_group.inputs.new(type='NodeSocketFloat', name="Current Texel Cone Offset")
        new_node_group.inputs.new(type='NodeSocketFloat', name="Step Height")
    if bpy.app.version >= (4, 0, 0):
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Finished", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Next Height", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Next Texel Height", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Next Texel Cone Ratio", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Next Texel Cone Offset", in_out='OUTPUT')
    else:
        new_node_group.outputs.new(type='NodeSocketFloat', name="Finished")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Next Height")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Next Texel Height")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Next Texel Cone Ratio")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Next Texel Cone Offset")

    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="NodeFrame")
    node.label = "Offset Cone Step next"
    node.location = (-1820, -1560)
    node.label_size = 20
    node.shrink = True
    new_nodes["Frame"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "Greater of depth step and cone step"
    node.location = (-1020, -1220)
    node.label_size = 20
    node.shrink = True
    new_nodes["Frame.001"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "If Next Depth below surface"
    node.location = (860, -480)
    node.label_size = 20
    node.shrink = True
    new_nodes["Frame.002"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "Interpolate Step"
    node.location = (80, -860)
    node.label_size = 20
    node.shrink = True
    new_nodes["Frame.003"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "If begin finished"
    node.location = (1300, -400)
    node.label_size = 20
    node.shrink = True
    new_nodes["Frame.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "ray_ratio"
    node.location = (-2180, -1480)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-2360, -1480)
    node.operation = "DIVIDE"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "incoming X"
    node.location = (-2740, -1400)
    node.operation = "DOT_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "incoming Y"
    node.location = (-2740, -1540)
    node.operation = "DOT_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "incoming Z"
    node.location = (-2740, -1680)
    node.operation = "DOT_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-2540, -1480)
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2360, -1860)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Ensure > 0"
    node.location = (-2180, -1860)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2000, -1480)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2000, -1860)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "d"
    node.location = (-1600, -1620)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, -1620)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2540, -1860)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1400, -1660)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1160, -1100)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1160, -1280)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-980, -1280)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-980, -1100)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, -640)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 1.570796
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, -640)
    node.operation = "TANGENT"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, -640)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -680)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -500)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -880)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -1060)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (700, -840)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If Next Depth >= Next Texel Depth"
    node.location = (700, -660)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "before_depth"
    node.location = (-280, -1220)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-100, -1220)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "weight"
    node.location = (80, -1060)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "1 - weight"
    node.location = (80, -880)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "final_depth"
    node.location = (440, -880)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (260, -1060)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "after_depth"
    node.location = (-280, -1060)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -580)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Depth"
    node.location = (1360, -400)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.030"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Texel Depth"
    node.location = (1360, -760)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -940)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If Finished = True"
    node.location = (1180, -560)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.033"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -740)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If next depth below surface"
    node.location = (1360, -140)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If next depth below surface"
    node.location = (1000, -180)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-980, -660)
    node.node_tree = bpy.data.node_groups.get(PARALLAX_MAP_MAT_NG_NAME)
    new_nodes["Group.ParallaxMap"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "Next texel"
    node.location = (-720, -800)
    node.node_tree = custom_data["custom_group_node"].node_tree
    new_nodes["Group.OCPOM_Input"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-980, -900)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.038"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, -800)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.039"] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-360, -840)
    new_nodes["Reroute"] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-2680, -1060)
    new_nodes["Reroute.001"] = node

    node = tree_nodes.new(type="NodeReroute")
    node.location = (-2680, -1000)
    new_nodes["Reroute.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2880, -880)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.040"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2880, -1040)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.041"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1600, -500)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.042"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1600, -340)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = -1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.043"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-3100, -820)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1800, -380)
    new_nodes["Group Output"] = node

    # parenting of nodes
    new_nodes["Vector Math"].parent = new_nodes["Frame"]
    new_nodes["Vector Math.001"].parent = new_nodes["Frame"]
    new_nodes["Vector Math.002"].parent = new_nodes["Frame"]
    new_nodes["Vector Math.003"].parent = new_nodes["Frame"]
    new_nodes["Vector Math.004"].parent = new_nodes["Frame"]
    new_nodes["Combine XYZ"].parent = new_nodes["Frame"]
    new_nodes["Math.001"].parent = new_nodes["Frame"]
    new_nodes["Math.002"].parent = new_nodes["Frame"]
    new_nodes["Math.003"].parent = new_nodes["Frame"]
    new_nodes["Math.004"].parent = new_nodes["Frame"]
    new_nodes["Math.005"].parent = new_nodes["Frame"]
    new_nodes["Math.006"].parent = new_nodes["Frame"]
    new_nodes["Math.007"].parent = new_nodes["Frame"]
    new_nodes["Math.008"].parent = new_nodes["Frame"]
    new_nodes["Math.009"].parent = new_nodes["Frame.001"]
    new_nodes["Math.010"].parent = new_nodes["Frame.001"]
    new_nodes["Math.011"].parent = new_nodes["Frame.001"]
    new_nodes["Math.012"].parent = new_nodes["Frame.001"]
    new_nodes["Math.016"].parent = new_nodes["Frame.002"]
    new_nodes["Math.017"].parent = new_nodes["Frame.002"]
    new_nodes["Math.018"].parent = new_nodes["Frame.002"]
    new_nodes["Math.019"].parent = new_nodes["Frame.002"]
    new_nodes["Math.020"].parent = new_nodes["Frame.002"]
    new_nodes["Math.021"].parent = new_nodes["Frame.002"]
    new_nodes["Math.022"].parent = new_nodes["Frame.003"]
    new_nodes["Math.023"].parent = new_nodes["Frame.003"]
    new_nodes["Math.024"].parent = new_nodes["Frame.003"]
    new_nodes["Math.025"].parent = new_nodes["Frame.003"]
    new_nodes["Math.026"].parent = new_nodes["Frame.003"]
    new_nodes["Math.027"].parent = new_nodes["Frame.003"]
    new_nodes["Math.028"].parent = new_nodes["Frame.003"]
    new_nodes["Math.029"].parent = new_nodes["Frame.004"]
    new_nodes["Math.030"].parent = new_nodes["Frame.004"]
    new_nodes["Math.031"].parent = new_nodes["Frame.004"]
    new_nodes["Math.032"].parent = new_nodes["Frame.004"]
    new_nodes["Math.033"].parent = new_nodes["Frame.004"]
    new_nodes["Math.034"].parent = new_nodes["Frame.004"]

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Reroute"].outputs[0], new_nodes["Math.037"].inputs[1])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.035"].inputs[1])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.036"].inputs[1])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Reroute"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Reroute"].outputs[0], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Reroute"].outputs[0], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.012"].inputs[2])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.004"].outputs[1], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Reroute.002"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Reroute.002"].outputs[0], new_nodes["Math.008"].inputs[2])
    tree_links.new(new_nodes["Reroute.001"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.030"].inputs[2])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.034"].inputs[1])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.030"].inputs[0])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.033"].inputs[0])
    tree_links.new(new_nodes["Reroute.002"].outputs[0], new_nodes["Math.030"].inputs[1])
    tree_links.new(new_nodes["Math.043"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Math.031"].inputs[2])
    tree_links.new(new_nodes["Reroute.001"].outputs[0], new_nodes["Math.031"].inputs[1])
    tree_links.new(new_nodes["Math.042"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.017"].inputs[2])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.020"].inputs[1])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.029"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.018"].inputs[2])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.032"].inputs[1])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.024"].inputs[1])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.027"].inputs[1])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.026"].inputs[2])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.028"].inputs[1])
    tree_links.new(new_nodes["Reroute.002"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Reroute.001"].outputs[0], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Reroute.002"].outputs[0], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.041"].inputs[0])
    tree_links.new(new_nodes["Math.041"].outputs[0], new_nodes["Reroute.001"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.038"].inputs[0])
    tree_links.new(new_nodes["Math.039"].outputs[0], new_nodes["Reroute"].inputs[0])
    tree_links.new(new_nodes["Math.040"].outputs[0], new_nodes["Reroute.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.040"].inputs[0])
    tree_links.new(new_nodes["Math.030"].outputs[0], new_nodes["Math.043"].inputs[0])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Math.042"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.ParallaxMap"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.ParallaxMap"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.ParallaxMap"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.ParallaxMap"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.ParallaxMap"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.ParallaxMap"].inputs[5])
    tree_links.new(new_nodes["Math.038"].outputs[0], new_nodes["Group.ParallaxMap"].inputs[6])

    tree_links.new(new_nodes["Group.ParallaxMap"].outputs[0], new_nodes["Group.OCPOM_Input"].inputs[0])
    tree_links.new(new_nodes["Group.OCPOM_Input"].outputs[3], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Group.OCPOM_Input"].outputs[2], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Group.OCPOM_Input"].outputs[0], new_nodes["Math.039"].inputs[0])
    tree_links.new(new_nodes["Group.OCPOM_Input"].outputs[1], new_nodes["Math.013"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_mat_ng_offset_conestep_pom(custom_data):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=OFFSET_CONESTEP_POM_MAT_NG_NAME, type='ShaderNodeTree')

    # remove old group inputs and outputs
    if bpy.app.version >= (4, 0, 0):
        for item in new_node_group.interface.items_tree:
            if item.item_type == 'SOCKET':
                new_node_group.interface.remove(item)
    else:
        new_node_group.inputs.clear()
        new_node_group.outputs.clear()
    # create new group inputs and outputs
    new_in_socket = {}
    if bpy.app.version >= (4, 0, 0):
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="UV Input", in_out='INPUT')
        new_in_socket[1] = new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Aspect Ratio", in_out='INPUT')
        new_in_socket[2] = new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Tangent U", in_out='INPUT')
        new_in_socket[3] = new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Tangent V", in_out='INPUT')
        new_in_socket[4] = new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Normal", in_out='INPUT')
        new_in_socket[5] = new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="Incoming", in_out='INPUT')
        new_in_socket[6] = new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Total Step Height", in_out='INPUT')
    else:
        new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
        new_in_socket[1] = new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
        new_in_socket[2] = new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U")
        new_in_socket[3] = new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V")
        new_in_socket[4] = new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
        new_in_socket[5] = new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
        new_in_socket[6] = new_node_group.inputs.new(type='NodeSocketFloat', name="Total Step Height")
    new_in_socket[1].default_value = (1.000000, 1.000000, 1.000000)
    new_in_socket[2].default_value = (1.000000, 0.000000, 0.000000)
    new_in_socket[3].default_value = (0.000000, 1.000000, 0.000000)
    new_in_socket[4].default_value = (0.000000, 0.000000, 1.000000)
    new_in_socket[5].default_value = (0.000000, 0.000000, 1.000000)
    new_in_socket[6].min_value = 0.000000
    new_in_socket[6].default_value = 0.005000
    if bpy.app.version >= (4, 0, 0):
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="UV Output", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Height Output", in_out='OUTPUT')
    else:
        new_node_group.outputs.new(type='NodeSocketVector', name="UV Output")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Height Output")

    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1580, 40)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = math.pi / 2.0
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1400, 40)
    node.operation = "TANGENT"
    node.use_clamp = False
    new_nodes["OuterMathTangent"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1220, 40)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["OuterMathConeRatioDivide"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If begin finished"
    node.location = (-1200, -120)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1400, -360)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[1].default_value = custom_data["sample_num"]
    new_nodes["Math.999"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1800, -160)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-340 + (custom_data["sample_num"]-1) * 200, 40)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-1580, -120)
    node.node_tree = custom_data["custom_group_node"].node_tree
    new_nodes["SampleOuterGroup"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-980, 40)
    node.node_tree = custom_data["iterate_mat_ng"]
    node.inputs[7].default_value = 0.000000
    new_nodes["IterateGroup.0"] = node

    # create total number of samples, less one, because first node created already
    for c in range(custom_data["sample_num"]-1):
        node = tree_nodes.new(type="ShaderNodeGroup")
        node.location = (-760 + c * 200, 40)
        node.node_tree = custom_data["iterate_mat_ng"]
        new_nodes["IterateGroup." + str(c+1)] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-920 + custom_data["sample_num"] * 200, 40)
    node.node_tree = bpy.data.node_groups.get(PARALLAX_MAP_MAT_NG_NAME)
    new_nodes["FinalPOM_Group"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["OuterMathTangent"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.999"].inputs[0])

    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["SampleOuterGroup"].inputs[0])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[1], new_nodes["Math.009"].inputs[0])

    tree_links.new(new_nodes["SampleOuterGroup"].outputs[0], new_nodes["IterateGroup.0"].inputs[8])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[3], new_nodes["IterateGroup.0"].inputs[10])

    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["IterateGroup.0"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["IterateGroup.0"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["IterateGroup.0"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["IterateGroup.0"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["IterateGroup.0"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["IterateGroup.0"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["IterateGroup.0"].inputs[6])

    tree_links.new(new_nodes["OuterMathTangent"].outputs[0], new_nodes["OuterMathConeRatioDivide"].inputs[0])
    tree_links.new(new_nodes["OuterMathConeRatioDivide"].outputs[0], new_nodes["IterateGroup.0"].inputs[9])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[2], new_nodes["OuterMathConeRatioDivide"].inputs[1])

    tree_links.new(new_nodes["Math.999"].outputs[0], new_nodes["IterateGroup.0"].inputs[11])

    # create needed number of sample iteration nodes
    prev_node = new_nodes["IterateGroup.0"]
    for c in range(custom_data["sample_num"]-1):
        next_node = new_nodes["IterateGroup."+str(c+1)]
        tree_links.new(prev_node.outputs[0], next_node.inputs[0])
        tree_links.new(new_nodes["Group Input"].outputs[0], next_node.inputs[1])
        tree_links.new(new_nodes["Group Input"].outputs[1], next_node.inputs[2])
        tree_links.new(new_nodes["Group Input"].outputs[2], next_node.inputs[3])
        tree_links.new(new_nodes["Group Input"].outputs[3], next_node.inputs[4])
        tree_links.new(new_nodes["Group Input"].outputs[4], next_node.inputs[5])
        tree_links.new(new_nodes["Group Input"].outputs[5], next_node.inputs[6])
        tree_links.new(prev_node.outputs[1], next_node.inputs[7])
        tree_links.new(prev_node.outputs[2], next_node.inputs[8])
        tree_links.new(prev_node.outputs[3], next_node.inputs[9])
        tree_links.new(prev_node.outputs[4], next_node.inputs[10])
        tree_links.new(new_nodes["Math.999"].outputs[0], next_node.inputs[11])

        prev_node = next_node

    # create link from final iteration node to the height output
    tree_links.new(prev_node.outputs[2], new_nodes["Group Output"].inputs[1])

    # create links for OCPOM UV output
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["FinalPOM_Group"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["FinalPOM_Group"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["FinalPOM_Group"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["FinalPOM_Group"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["FinalPOM_Group"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["FinalPOM_Group"].inputs[5])

    # create link from last iteration node to final POM node
    tree_links.new(prev_node.outputs[2], new_nodes["FinalPOM_Group"].inputs[6])
    # create UV output link
    tree_links.new(new_nodes["FinalPOM_Group"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_ocpom_inputs_simple(node_tree, ocpom_mat_ng, active_obj):
    tree_nodes = node_tree.nodes

    # create nodes
    new_nodes = {}

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (0, 0)
    node.node_tree = ocpom_mat_ng
    # set this OCPOM node to be active node
    node_tree.nodes.active = node
    new_nodes[OCPOM_NODENAME] = node

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
    tree_links.new(new_nodes[UV_INPUT_NODENAME].outputs[2], new_nodes[OCPOM_NODENAME].inputs[0])
    tree_links.new(new_nodes[TANGENT_U_INPUT_NODENAME].outputs[0], new_nodes[OCPOM_NODENAME].inputs[2])
    tree_links.new(new_nodes[TANGENT_V_INPUT_NODENAME].outputs[0], new_nodes[OCPOM_NODENAME].inputs[3])
    tree_links.new(new_nodes[GEOMETRY_INPUT_NODENAME].outputs[1], new_nodes[OCPOM_NODENAME].inputs[4])
    tree_links.new(new_nodes[GEOMETRY_INPUT_NODENAME].outputs[4], new_nodes[OCPOM_NODENAME].inputs[5])

def create_ocpom_inputs_mapping(node_tree, ocpom_mat_ng, active_obj):
    tree_nodes = node_tree.nodes

    # create nodes
    new_nodes = {}

    # create nodes
    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = "Tangent U"
    node.location = (-380, -120)
    node.direction_type = "UV_MAP"
    node.uv_map = get_tangent_map_name("U", active_obj)
    new_nodes["Tangent"] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = "Tangent V"
    node.location = (-380, -220)
    node.direction_type = "UV_MAP"
    node.uv_map = get_tangent_map_name("V", active_obj)
    new_nodes["Tangent.001"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (-380, -320)
    new_nodes["Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Degrees to Radians"
    node.hide = True
    node.location = (-380, -80)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = math.pi / 180.0
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-580, 0)
    node.from_instancer = False
    new_nodes["Texture Coordinate"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "UV Scale"
    node.location = (-580, -240)
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 1.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.hide = True
    node.location = (-180, -160)
    node.invert = True
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.hide = True
    node.location = (-180, -240)
    node.invert = True
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "UV Scale, UV Locate"
    node.hide = True
    node.location = (-380, -40)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.label = "UV Rotate"
    node.hide = True
    node.location = (-180, -80)
    node.invert = False
    node.rotation_type = "AXIS_ANGLE"
    node.inputs[2].default_value = (0.0, 0.0, 1.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (0, 0)
    node.node_tree = ocpom_mat_ng
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "UV Locate"
    node.location = (-580, -360)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "UV Rotation (degrees)"
    node.location = (-580, -480)
    node.outputs[0].default_value = 0.000000
    new_nodes["Value.001"] = node

    # offset node locations relative to view center
    view_center = (node_tree.view_center[0] / 1.5, node_tree.view_center[1] / 1.5)
    for n in new_nodes.values():
        n.location = (n.location[0] + view_center[0], n.location[1] + view_center[1])

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate.002"].outputs[0], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Vector Rotate.001"].outputs[0], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Tangent"].outputs[0], new_nodes["Vector Rotate.002"].inputs[0])
    tree_links.new(new_nodes["Tangent.001"].outputs[0], new_nodes["Vector Rotate.001"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Vector Rotate"].inputs[3])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Vector Rotate.002"].inputs[3])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Vector Rotate.001"].inputs[3])
    tree_links.new(new_nodes["Geometry"].outputs[3], new_nodes["Vector Rotate.002"].inputs[2])
    tree_links.new(new_nodes["Geometry"].outputs[3], new_nodes["Vector Rotate.001"].inputs[2])
    tree_links.new(new_nodes["Texture Coordinate"].outputs[2], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Value.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math"].inputs[2])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Rotate"].inputs[1])

def create_ocpom_node(active_obj, node_tree, override_create, ocpom_mapping_nodes, custom_group_node, sample_num):
    ensure_node_group(override_create, PARALLAX_MAP_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)
    # these node groups need to be re-created every time, because they use the custom group node
    custom_data = {
        "custom_group_node": custom_group_node,
        "sample_num": sample_num,
    }

    iterate_mat_ng = create_mat_ng_iterate(custom_data)
    custom_data["iterate_mat_ng"] = iterate_mat_ng
    ocpom_mat_ng = create_mat_ng_offset_conestep_pom(custom_data)

    if ocpom_mapping_nodes:
        create_ocpom_inputs_mapping(node_tree, ocpom_mat_ng, active_obj)
    else:
        create_ocpom_inputs_simple(node_tree, ocpom_mat_ng, active_obj)

def create_blank_node_group(height_img, height_mult):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=BLANK_NODE_GROUP_NAME, type='ShaderNodeTree')

    # remove old group inputs and outputs
    if bpy.app.version >= (4, 0, 0):
        for item in new_node_group.interface.items_tree:
            if item.item_type == 'SOCKET':
                new_node_group.interface.remove(item)
    else:
        new_node_group.inputs.clear()
        new_node_group.outputs.clear()
    # create new group inputs and outputs
    new_in_socket = {}
    if bpy.app.version >= (4, 0, 0):
        new_node_group.interface.new_socket(socket_type='NodeSocketVector', name="UV Input", in_out='INPUT')
    else:
        new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_out_socket = {}
    if bpy.app.version >= (4, 0, 0):
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Height", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Cone Ratio Angle", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Cone Ratio Divisor", in_out='OUTPUT')
        new_node_group.interface.new_socket(socket_type='NodeSocketFloat', name="Cone Offset", in_out='OUTPUT')
    else:
        new_node_group.outputs.new(type='NodeSocketFloat', name="Height")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Cone Ratio Angle")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Cone Ratio Divisor")
        new_node_group.outputs.new(type='NodeSocketFloat', name="Cone Offset")

    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-300, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (560, 0)
    node.inputs[0].default_value = -0.05
    node.inputs[1].default_value = 0.9
    node.inputs[2].default_value = 1.0
    node.inputs[3].default_value = 0.001
    new_nodes["Group Output"] = node

    # if height_img given then create nodes to implement default height Image Texture inputs
    if height_img != None:
        node = tree_nodes.new(type="ShaderNodeTexImage")
        node.location = (-100, 0)
        node.image = height_img
        new_nodes["Image Texture"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (180, 0)
        node.operation = "SUBTRACT"
        node.use_clamp = False
        node.inputs[1].default_value = 1.000000
        new_nodes["Math"] = node

        node = tree_nodes.new(type="ShaderNodeMath")
        node.location = (360, 0)
        node.operation = "MULTIPLY"
        node.use_clamp = False
        node.inputs[1].default_value = height_mult
        new_nodes["Math.001"] = node

        tree_links = new_node_group.links
        tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Image Texture"].inputs[0])
        tree_links.new(new_nodes["Image Texture"].outputs[0], new_nodes["Math"].inputs[0])
        tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
        tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_blank_ocpom_input_node(node_tree, height_img, height_mult):
    new_blank_node_group = create_blank_node_group(height_img, height_mult)
    if new_blank_node_group is None:
        print("ERROR: Create new blank node group failed.")
        return None
    # create a node group type node with group set to the new blank group
    tree_nodes = node_tree.nodes
    view_center = (node_tree.view_center[0] / 1.5, node_tree.view_center[1] / 1.5)
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (view_center[0], -460 + view_center[1])
    node.node_tree = bpy.data.node_groups.get(new_blank_node_group.name)

    return node

class POMSTER_AddOCPOM_Node(bpy.types.Operator):
    bl_description = "With selected active node as input, create Offset Conestep Parallax Occlusion Map (OCPOM) " \
        "node. Active node needs at least 1 vector input and 4 float outputs. Creates default OCPOM input if no " \
        "node is selected"
    bl_idname = "pomster.create_offset_conestep_pom_nodes"
    bl_label = "Offset Conestep POM"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        tree_nodes = context.space_data.edit_tree.nodes
        # check that the material has a nodes tree
        if tree_nodes is None:
            self.report({'ERROR'}, "Cannot create Offset Conestep Parallax Occlusion Map nodes because current " +
                        "material doesn't use nodes. Enable material's 'Use Nodes' option to continue.")
            return {'CANCELLED'}
        # get active node before adding nodes and/or changing node tree
        active_node = tree_nodes.active
        # create a blank node if active node is not available or if active node is wrong type
        if active_node is None or active_node.select == False or active_node.bl_idname != 'ShaderNodeGroup':
            # deselect all nodes
            for n in tree_nodes: n.select = False

            blank_node = create_blank_ocpom_input_node(context.space_data.edit_tree, scn.POMster.height_img_input,
                                                       scn.POMster.default_height_multiplier)
            # blank OCPOM input node was created, so use default input/output indexes to create OCPOM Node Group node
            create_ocpom_node(context.active_object, context.space_data.edit_tree, scn.POMster.nodes_override_create,
                scn.POMster.ocpom_mapping_nodes, blank_node, scn.POMster.num_samples)
        else:
            # check custom node's type, inputs and report any errors to user
            # check user selected node to ensure correct type of inputs
            if not hasattr(active_node.inputs[0], 'default_value') or \
                not hasattr(active_node.inputs[0].default_value, '__len__') or \
                len(active_node.inputs[0].default_value) != 3 or \
                not isinstance(active_node.inputs[0].default_value[0], float):
                self.report({'ERROR'}, "Cannot create Offset Conestep Parallax Occlusion Map nodes because active " +
                            "group node's input number 1 is not a Vector type.")
                return {'CANCELLED'}

            # check custom node's type outputs, and report any errors to user
            # check user selected node to ensure minimum amount of outputs for height output
            num_outputs = len(active_node.outputs)
            if num_outputs < 1 or \
                not isinstance(active_node.outputs[0].default_value, float):
                self.report({'ERROR'}, "Cannot get Height output, cannot create Offset Conestep Parallax Occlusion Map " +
                            "with output number 1.")
                return {'CANCELLED'}
            # check user selected node to ensure minimum amount of outputs for cone ratio angle output
            if num_outputs < 2 or \
                    not isinstance(active_node.outputs[1].default_value, float):
                self.report({'ERROR'}, "Cannot get Cone Ratio Angle output, cannot create Offset Conestep Parallax " +
                            "Occlusion Map with output number 2.")
                return {'CANCELLED'}
            # check user selected node to ensure minimum amount of outputs for cone ratio divisor output
            if num_outputs < 3 or \
                    not isinstance(active_node.outputs[2].default_value, float):
                self.report({'ERROR'}, "Cannot get Cone Ratio Divisor output, cannot create Offset Conestep Parallax "+
                            "Occlusion Map with output number 3.")
                return {'CANCELLED'}
            # check user selected node to ensure minimum amount of outputs for cone offset output
            if num_outputs < 4 or \
                    not isinstance(active_node.outputs[3].default_value, float):
                self.report({'ERROR'}, "Cannot get Cone Offset output, cannot create Offset Conestep Parallax " +
                            "Occlusion Map with output number 4.")
                return {'CANCELLED'}

            # deselect all nodes
            for n in tree_nodes: n.select = False

            # get the UI panel properties for index numbers and use them to create OCPOM Node Group node
            create_ocpom_node(context.active_object, context.space_data.edit_tree, scn.POMster.nodes_override_create,
                scn.POMster.ocpom_mapping_nodes, active_node, scn.POMster.num_samples)
        return {'FINISHED'}
