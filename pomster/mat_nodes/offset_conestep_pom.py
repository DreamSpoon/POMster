
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

from .node_other import (get_tangent_map_name, ensure_node_group, MAT_NG_NAME_SUFFIX)
from .parallax_map import (create_mat_ng_parallax_map, PARALLAX_MAP_MAT_NG_NAME)

OFFSET_CONESTEP_POM_MAT_NG_NAME = "OffsetConestepPOM" + MAT_NG_NAME_SUFFIX
ITERATE_MAT_NG_NAME = "_iterate" + MAT_NG_NAME_SUFFIX
BLANK_NODE_GROUP_NAME = "InputOCPOM" + MAT_NG_NAME_SUFFIX

OCPOM_NODENAME = "OCPOM Node"
UV_INPUT_NODENAME = "UV Input"
TANGENT_U_INPUT_NODENAME = "Tangent U"
TANGENT_V_INPUT_NODENAME = "Tangent V"
GEOMETRY_INPUT_NODENAME = "Geometry Input"
DEPTH_STEP_INPUT_NODENAME = "Depth Step"

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
    new_node_group.inputs.new(type='NodeSocketFloat', name="Finished")
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V")
    new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Current Depth")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Current Texel Depth")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Current Texel Cone Ratio")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Current Texel Cone Offset")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Index")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Total")
    new_node_group.inputs.new(type='NodeSocketFloat', name="First Step Depth")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Last Step Depth")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Finished")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Next Depth")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Next Texel Depth")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Next Texel Cone Ratio")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Next Texel Cone Offset")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Index")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Total")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-980, -800)
    node.node_tree = bpy.data.node_groups.get(PARALLAX_MAP_MAT_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "Next texel"
    node.location = (-720, -800)
    node.node_tree = custom_data["custom_group_node"].node_tree
    new_nodes["SampleInnerGroup"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "Offset Cone Step next"
    node.location = (-1820, -1560)
    node.shrink = True
    new_nodes["Frame.001"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "Greater of depth step and cone step"
    node.location = (-1020, -1220)
    node.shrink = True
    new_nodes["Frame"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "If Next Depth below surface"
    node.location = (860, -480)
    node.shrink = True
    new_nodes["Frame.003"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "Interpolate Step"
    node.location = (80, -860)
    node.shrink = True
    new_nodes["Frame.004"] = node

    node = tree_nodes.new(type="NodeFrame")
    node.label = "If begin finished"
    node.location = (1300, -400)
    node.shrink = True
    new_nodes["Frame.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Depth step next"
    node.location = (-1400, -1100)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-1580, -1100)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 1.000000
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "ray_ratio"
    node.location = (-2180, -1480)
    node.operation = "LENGTH"
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-2360, -1480)
    node.operation = "DIVIDE"
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "incoming X"
    node.location = (-2740, -1400)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "incoming Y"
    node.location = (-2740, -1540)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "incoming Z"
    node.location = (-2740, -1680)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-2540, -1480)
    node.inputs[2].default_value = 0.000000
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2360, -1860)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Ensure > 0"
    node.location = (-2180, -1860)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2000, -1480)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2000, -1860)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "d"
    node.location = (-1600, -1620)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, -1620)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2540, -1860)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1400, -1660)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1160, -1100)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1160, -1280)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-980, -1280)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-980, -1100)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, -640)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = math.pi / 2.0
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, -640)
    node.operation = "TANGENT"
    node.use_clamp = False
    new_nodes["InnerMathTangent"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, -640)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["InnerMathConeRatioDivide"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -680)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -500)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -880)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (880, -1060)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (700, -840)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If Next Depth >= Next Texel Depth"
    node.location = (700, -660)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Next Sample Index"
    node.location = (1620, -600)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "before_depth"
    node.location = (-280, -1220)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-100, -1220)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.030"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "weight"
    node.location = (80, -1060)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math.033"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "1 - weight"
    node.location = (80, -880)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "final_depth"
    node.location = (440, -880)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (260, -1060)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "after_depth"
    node.location = (-280, -1060)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -580)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Depth"
    node.location = (1360, -400)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Texel Depth"
    node.location = (1360, -760)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -940)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If Finished = True"
    node.location = (1180, -560)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -740)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If next depth below surface"
    node.location = (1360, -140)
    node.operation = "ADD"
    node.use_clamp = True
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If next depth below surface"
    node.location = (1000, -180)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-3100, -820)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1620, -380)
    new_nodes["Group Output"] = node

    # parenting of nodes
    new_nodes["Vector Math.003"].parent = new_nodes["Frame.001"]
    new_nodes["Vector Math.004"].parent = new_nodes["Frame.001"]
    new_nodes["Vector Math"].parent = new_nodes["Frame.001"]
    new_nodes["Vector Math.001"].parent = new_nodes["Frame.001"]
    new_nodes["Vector Math.002"].parent = new_nodes["Frame.001"]
    new_nodes["Combine XYZ"].parent = new_nodes["Frame.001"]
    new_nodes["Math.011"].parent = new_nodes["Frame.001"]
    new_nodes["Math.012"].parent = new_nodes["Frame.001"]
    new_nodes["Math.013"].parent = new_nodes["Frame.001"]
    new_nodes["Math.014"].parent = new_nodes["Frame.001"]
    new_nodes["Math.015"].parent = new_nodes["Frame.001"]
    new_nodes["Math.016"].parent = new_nodes["Frame.001"]
    new_nodes["Math.018"].parent = new_nodes["Frame.001"]
    new_nodes["Math.017"].parent = new_nodes["Frame.001"]
    new_nodes["Math.004"].parent = new_nodes["Frame"]
    new_nodes["Math.005"].parent = new_nodes["Frame"]
    new_nodes["Math.007"].parent = new_nodes["Frame"]
    new_nodes["Math.006"].parent = new_nodes["Frame"]
    new_nodes["Math.028"].parent = new_nodes["Frame.003"]
    new_nodes["Math.027"].parent = new_nodes["Frame.003"]
    new_nodes["Math.031"].parent = new_nodes["Frame.003"]
    new_nodes["Math.032"].parent = new_nodes["Frame.003"]
    new_nodes["Math.024"].parent = new_nodes["Frame.003"]
    new_nodes["Math.023"].parent = new_nodes["Frame.003"]
    new_nodes["Math.029"].parent = new_nodes["Frame.004"]
    new_nodes["Math.030"].parent = new_nodes["Frame.004"]
    new_nodes["Math.033"].parent = new_nodes["Frame.004"]
    new_nodes["Math.034"].parent = new_nodes["Frame.004"]
    new_nodes["Math.035"].parent = new_nodes["Frame.004"]
    new_nodes["Math.036"].parent = new_nodes["Frame.004"]
    new_nodes["Math.037"].parent = new_nodes["Frame.004"]
    new_nodes["Math.022"].parent = new_nodes["Frame.002"]
    new_nodes["Math.021"].parent = new_nodes["Frame.002"]
    new_nodes["Math.025"].parent = new_nodes["Frame.002"]
    new_nodes["Math.026"].parent = new_nodes["Frame.002"]
    new_nodes["Math.019"].parent = new_nodes["Frame.002"]
    new_nodes["Math.020"].parent = new_nodes["Frame.002"]

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.001"].inputs[5])

    tree_links.new(new_nodes["Group.001"].outputs[0],
                   new_nodes["SampleInnerGroup"].inputs[custom_data["uv_input_index"]])
    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["depth_output_index"]],
                   new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["cone_offset_output_index"]],
                   new_nodes["Group Output"].inputs[4])

    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["InnerMathTangent"].inputs[0])

    tree_links.new(new_nodes["InnerMathTangent"].outputs[0], new_nodes["InnerMathConeRatioDivide"].inputs[0])
    tree_links.new(new_nodes["InnerMathConeRatioDivide"].outputs[0], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["cone_ratio_divisor_output_index"]],
                   new_nodes["InnerMathConeRatioDivide"].inputs[1])

    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["depth_output_index"]],
                   new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["depth_output_index"]],
                   new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["depth_output_index"]],
                   new_nodes["Math.031"].inputs[1])
    tree_links.new(new_nodes["SampleInnerGroup"].outputs[custom_data["cone_ratio_angle_output_index"]],
                   new_nodes["Math.009"].inputs[0])

    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.006"].inputs[2])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[1], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.017"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.021"].inputs[2])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.020"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.025"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.027"].inputs[2])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.024"].inputs[1])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.028"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.027"].inputs[1])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Math.031"].inputs[2])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.030"].inputs[0])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.030"].inputs[1])
    tree_links.new(new_nodes["Math.030"].outputs[0], new_nodes["Math.033"].inputs[1])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.033"].inputs[0])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.034"].inputs[1])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Math.036"].inputs[1])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Math.035"].inputs[2])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.035"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.037"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.029"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.035"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.028"].inputs[1])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.032"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_mat_ng_offset_conestep_pom(custom_data):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=OFFSET_CONESTEP_POM_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V")
    new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
    new_node_group.inputs.new(type='NodeSocketFloat', name="First Step Depth")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Last Step Depth")
    new_node_group.outputs.new(type='NodeSocketVector', name="UV Output")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Depth Output")
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
    node.inputs[11].default_value = 1.000000
    node.inputs[12].default_value = custom_data["sample_num"]
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

    tree_links.new(new_nodes["Group Input"].outputs[0],
                   new_nodes["SampleOuterGroup"].inputs[custom_data["uv_input_index"]])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[custom_data["depth_output_index"]],
                   new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[custom_data["cone_ratio_angle_output_index"]],
                   new_nodes["Math.009"].inputs[0])

    tree_links.new(new_nodes["SampleOuterGroup"].outputs[custom_data["depth_output_index"]],
                   new_nodes["IterateGroup.0"].inputs[8])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[custom_data["cone_offset_output_index"]],
                   new_nodes["IterateGroup.0"].inputs[10])

    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["IterateGroup.0"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["IterateGroup.0"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["IterateGroup.0"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["IterateGroup.0"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["IterateGroup.0"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["IterateGroup.0"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["IterateGroup.0"].inputs[6])

    tree_links.new(new_nodes["OuterMathTangent"].outputs[0], new_nodes["OuterMathConeRatioDivide"].inputs[0])
    tree_links.new(new_nodes["OuterMathConeRatioDivide"].outputs[0], new_nodes["IterateGroup.0"].inputs[9])
    tree_links.new(new_nodes["SampleOuterGroup"].outputs[custom_data["cone_ratio_divisor_output_index"]],
                   new_nodes["OuterMathConeRatioDivide"].inputs[1])

    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["IterateGroup.0"].inputs[13])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["IterateGroup.0"].inputs[14])

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
        tree_links.new(prev_node.outputs[5], next_node.inputs[11])
        tree_links.new(prev_node.outputs[6], next_node.inputs[12])
        tree_links.new(new_nodes["Group Input"].outputs[6], next_node.inputs[13])
        tree_links.new(new_nodes["Group Input"].outputs[7], next_node.inputs[14])
        prev_node = next_node

    # create link from final iteration node to the depth output
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

def create_ocpom_node(active_obj, node_tree, override_create, custom_group_node, sample_num, uv_input_index,
                      depth_output_index, cone_ratio_angle_output_index, cone_ratio_divisor_output_index,
                      cone_offset_output_index):
    ensure_node_group(override_create, PARALLAX_MAP_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)
    # these node groups need to be re-created every time, because they use the custom group node
    custom_data = {
        "custom_group_node": custom_group_node,
        "sample_num": sample_num,
        "uv_input_index": uv_input_index,
        "depth_output_index": depth_output_index,
        "cone_ratio_angle_output_index": cone_ratio_angle_output_index,
        "cone_ratio_divisor_output_index": cone_ratio_divisor_output_index,
        "cone_offset_output_index": cone_offset_output_index,
    }

    iterate_mat_ng = create_mat_ng_iterate(custom_data)
    custom_data["iterate_mat_ng"] = iterate_mat_ng
    ocpom_mat_ng = create_mat_ng_offset_conestep_pom(custom_data)

    tree_nodes = node_tree.nodes

    # create nodes
    new_nodes = {}

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = ocpom_mat_ng
    node.inputs[1].default_value = (1, 1, 1)
    node.inputs[2].default_value = (1, 0, 0)
    node.inputs[3].default_value = (0, 1, 0)
    node.inputs[4].default_value = (0, 0, 1)
    node.inputs[6].default_value = 0.003
    node.inputs[7].default_value = 0.003
    # set this OCPOM node to be active node
    node_tree.nodes.active = node
    new_nodes[OCPOM_NODENAME] = node

    # create nodes for OCPOM input
    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = ((node_tree.view_center[0] / 2.5)-220, (node_tree.view_center[1] / 2.5)+160)
    new_nodes[UV_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = TANGENT_U_INPUT_NODENAME
    node.location = ((node_tree.view_center[0] / 2.5)-220, (node_tree.view_center[1] / 2.5)-100)
    node.direction_type = "UV_MAP"
    node.uv_map = get_tangent_map_name("U", active_obj)
    new_nodes[TANGENT_U_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = TANGENT_V_INPUT_NODENAME
    node.location = ((node_tree.view_center[0] / 2.5)-220, (node_tree.view_center[1] / 2.5)-200)
    node.direction_type = "UV_MAP"
    node.uv_map = get_tangent_map_name("V", active_obj)
    new_nodes[TANGENT_V_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = ((node_tree.view_center[0] / 2.5)-220, (node_tree.view_center[1] / 2.5)-300)
    new_nodes[GEOMETRY_INPUT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = DEPTH_STEP_INPUT_NODENAME
    node.location = ((node_tree.view_center[0] / 2.5), (node_tree.view_center[1] / 2.5)-360)
    node.outputs[0].default_value = 0.002
    new_nodes[DEPTH_STEP_INPUT_NODENAME] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes[UV_INPUT_NODENAME].outputs[2], new_nodes[OCPOM_NODENAME].inputs[0])
    tree_links.new(new_nodes[TANGENT_U_INPUT_NODENAME].outputs[0], new_nodes[OCPOM_NODENAME].inputs[2])
    tree_links.new(new_nodes[TANGENT_V_INPUT_NODENAME].outputs[0], new_nodes[OCPOM_NODENAME].inputs[3])
    tree_links.new(new_nodes[GEOMETRY_INPUT_NODENAME].outputs[1], new_nodes[OCPOM_NODENAME].inputs[4])
    tree_links.new(new_nodes[GEOMETRY_INPUT_NODENAME].outputs[4], new_nodes[OCPOM_NODENAME].inputs[5])
    tree_links.new(new_nodes[DEPTH_STEP_INPUT_NODENAME].outputs[0], new_nodes[OCPOM_NODENAME].inputs[6])
    tree_links.new(new_nodes[DEPTH_STEP_INPUT_NODENAME].outputs[0], new_nodes[OCPOM_NODENAME].inputs[7])

def create_blank_node_group():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=BLANK_NODE_GROUP_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Depth")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cone Ratio Angle")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cone Ratio Divisor")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Cone Offset")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-200, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (540, 0)
    node.inputs[0].default_value = 0.05
    node.inputs[1].default_value = 0.9
    node.inputs[2].default_value = 1.0
    node.inputs[3].default_value = 0.001
    new_nodes["Group Output"] = node

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_blank_ocpom_input_node(node_tree):
    new_blank_node_group = create_blank_node_group()
    if new_blank_node_group is None:
        print("ERROR: Create new blank node group failed.")
        return None
    # create a node group type node with group set to the new blank group
    tree_nodes = node_tree.nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = ((node_tree.view_center[0] / 2.5), -460 + (node_tree.view_center[1] / 2.5))
    node.node_tree = bpy.data.node_groups.get(new_blank_node_group.name)

    return node

class POMSTER_AddOCPOM_Node(bpy.types.Operator):
    bl_description = "With active node as input, create Offset Conestep Parallax Occlusion Map (OCPOM) node. " \
        "Active node needs at least 1 vector input and 4 float outputs. Creates blank OCPOM input if needed"
    bl_idname = "pomster.create_offset_conestep_pom_nodes"
    bl_label = "Offset Conestep POM"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

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
        if active_node is None or active_node.bl_idname != 'ShaderNodeGroup':
            # deselect all nodes
            for n in tree_nodes: n.select = False

            blank_node = create_blank_ocpom_input_node(context.space_data.edit_tree)
            # blank OCPOM input node was created, so use default input/output indexes to create OCPOM Node Group node
            create_ocpom_node(context.active_object, context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate,
                blank_node, scn.POMSTER_NumSamples, 0, 0, 1, 2, 3)
        else:
            # check custom node's type, inputs and report any errors to user
            # check user selected node to ensure minimum amount of inputs
            if len(active_node.inputs) < scn.POMSTER_UV_InputIndex:
                self.report({'ERROR'}, "Cannot create Offset Conestep Parallax Occlusion Map nodes because active " +
                            "group node does not have enough inputs to get input number " +
                            str(scn.POMSTER_UV_InputIndex) + " .")
                return {'CANCELLED'}
            # check user selected node to ensure correct type of inputs
            if not hasattr(active_node.inputs[scn.POMSTER_UV_InputIndex-1], 'default_value') or \
                not hasattr(active_node.inputs[scn.POMSTER_UV_InputIndex-1].default_value, '__len__') or \
                len(active_node.inputs[scn.POMSTER_UV_InputIndex-1].default_value) != 3 or \
                not isinstance(active_node.inputs[scn.POMSTER_UV_InputIndex-1].default_value[0], float):
                self.report({'ERROR'}, "Cannot create Offset Conestep Parallax Occlusion Map nodes because active " +
                            "group node's input number " + str(scn.POMSTER_UV_InputIndex) + " is not a Vector type.")
                return {'CANCELLED'}

            # check custom node's type outputs, and report any errors to user
            # check user selected node to ensure minimum amount of outputs for depth output
            num_outputs = len(active_node.outputs)
            if num_outputs < scn.POMSTER_DepthOutputIndex or \
                    not isinstance(active_node.outputs[scn.POMSTER_DepthOutputIndex-1].default_value, float):
                self.report({'ERROR'}, "Cannot get Depth output, cannot create Offset Conestep Parallax Occlusion Map " +
                            "with output number " +
                            str(scn.POMSTER_DepthOutputIndex) + " .")
                return {'CANCELLED'}
            # check user selected node to ensure minimum amount of outputs for cone ratio angle output
            if num_outputs < scn.POMSTER_ConeRatioAngleOutputIndex or \
                    not isinstance(active_node.outputs[scn.POMSTER_ConeRatioAngleOutputIndex-1].default_value, float):
                self.report({'ERROR'}, "Cannot get Cone Ratio Angle output, cannot create Offset Conestep Parallax " +
                            "Occlusion Map with output number " + str(scn.POMSTER_ConeRatioAngleOutputIndex) + " .")
                return {'CANCELLED'}
            # check user selected node to ensure minimum amount of outputs for cone ratio divisor output
            if num_outputs < scn.POMSTER_ConeRatioDivisorOutputIndex or \
                    not isinstance(active_node.outputs[scn.POMSTER_ConeRatioDivisorOutputIndex-1].default_value, float):
                self.report({'ERROR'}, "Cannot get Cone Ratio Divisor output, cannot create Offset Conestep Parallax "+
                            "Occlusion Map with output number " + str(scn.POMSTER_ConeRatioDivisorOutputIndex) + " .")
                return {'CANCELLED'}
            # check user selected node to ensure minimum amount of outputs for cone offset output
            if num_outputs < scn.POMSTER_ConeOffsetOutputIndex or \
                    not isinstance(active_node.outputs[scn.POMSTER_ConeOffsetOutputIndex-1].default_value, float):
                self.report({'ERROR'}, "Cannot get Cone Offset output, cannot create Offset Conestep Parallax " +
                            "Occlusion Map with output number " + str(scn.POMSTER_ConeOffsetOutputIndex) + " .")
                return {'CANCELLED'}

            # deselect all nodes
            for n in tree_nodes: n.select = False

            # get the UI panel properties for index numbers and use them to create OCPOM Node Group node
            create_ocpom_node(context.active_object, context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate,
                active_node, scn.POMSTER_NumSamples, scn.POMSTER_UV_InputIndex-1, scn.POMSTER_DepthOutputIndex-1,
                scn.POMSTER_ConeRatioAngleOutputIndex-1, scn.POMSTER_ConeRatioDivisorOutputIndex-1,
                scn.POMSTER_ConeOffsetOutputIndex-1)
        return {'FINISHED'}
