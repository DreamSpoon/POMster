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
from .geo_nodes.shell_fringe import (create_prereq_shell_fringe_node_group, SHELL_ARRAY_GEO_NG_NAME,
    FRINGE_EXTRUDE_GEO_NG_NAME)

def create_obj_mod_geo_nodes_shell_fringe(node_group):
    # initialize variables
    new_nodes = {}
    node_group.inputs.clear()
    node_group.outputs.clear()
    node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_input = node_group.inputs.new(type='NodeSocketInt', name="Shell Count")
    new_input.min_value = 2
    new_input.default_value = 4
    node_group.inputs.new(type='NodeSocketBool', name="Delete Zero Index")
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Min Height")
    new_input.default_value = -0.050000
    node_group.inputs.new(type='NodeSocketFloat', name="Max Height")
    node_group.inputs.new(type='NodeSocketBool', name="Use Other Normal")
    node_group.inputs.new(type='NodeSocketVector', name="Other Normal")
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Max Stretch Factor")
    new_input.min_value = 0.000000
    new_input.default_value = 4.000000
    node_group.inputs.new(type='NodeSocketBool', name="Shell Geo Exclude")
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Shell Mat Exclude")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    node_group.inputs.new(type='NodeSocketBool', name="Fringe Geo Exclude")
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Fringe Mat Exclude")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    node_group.inputs.new(type='NodeSocketObject', name="Camera Object")
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Min Shell Angle Factor")
    new_input.min_value = 0.000000
    new_input.max_value = 2.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Max Shell Angle Factor")
    new_input.min_value = 0.000000
    new_input.max_value = 2.000000
    new_input.default_value = 2.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Min Fringe Angle Factor")
    new_input.min_value = 0.000000
    new_input.max_value = 2.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Max Fringe Angle Factor")
    new_input.min_value = 0.000000
    new_input.max_value = 2.000000
    new_input.default_value = 2.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Min Shell View Distance")
    new_input.min_value = 0.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Max Shell View Distance")
    new_input.min_value = 0.000000
    new_input.default_value = 340282346638528859811704183484516925440.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Min Fringe View Distance")
    new_input.min_value = 0.000000
    new_input = node_group.inputs.new(type='NodeSocketFloat', name="Max Fringe View Distance")
    new_input.min_value = 0.000000
    new_input.default_value = 340282346638528859811704183484516925440.000000
    node_group.inputs.new(type='NodeSocketVector', name="UV")
    node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    node_group.outputs.new(type='NodeSocketFloat', name="Shell Count")
    node_group.outputs.new(type='NodeSocketFloat', name="Min Height")
    node_group.outputs.new(type='NodeSocketFloat', name="Max Height")
    node_group.outputs.new(type='NodeSocketFloat', name="Shell Index")
    node_group.outputs.new(type='NodeSocketFloat', name="Shell Height")
    node_group.outputs.new(type='NodeSocketVector', name="Shell Offset")
    node_group.outputs.new(type='NodeSocketFloat', name="Is Fringe")
    node_group.outputs.new(type='NodeSocketFloat', name="Fringe Height")
    node_group.outputs.new(type='NodeSocketFloat', name="Shell Mat Exclude")
    node_group.outputs.new(type='NodeSocketFloat', name="Fringe Mat Exclude")
    node_group.outputs.new(type='NodeSocketVector', name="Original Position")
    node_group.outputs.new(type='NodeSocketVector', name="UV")
    tree_nodes = node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1340, -20)
    new_nodes["Position.002"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.location = (-1340, 160)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, -960)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1080, 0)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Shell Exclude"
    node.location = (-900, 200)
    node.data_type = "FLOAT"
    node.domain = "FACE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 0)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, -640)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, -480)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 1.570796
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, -800)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 1.570796
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, 0)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-260, 0)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="GeometryNodeJoinGeometry")
    node.location = (-260, 560)
    new_nodes["Join Geometry"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Is Fringe"
    node.location = (-260, 480)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 1.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (20, 240)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-620, -800)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 1.570796
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-620, -480)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 1.570796
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, -320)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-620, -320)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, -320)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Exclude by Angle"
    node.location = (-1080, -160)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1080, -320)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-1080, -940)
    new_nodes["Normal.001"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-1080, -1260)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1080, -1000)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1080, -1120)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-1080, -800)
    node.operation = "DOT_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1080, -640)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="GeometryNodeObjectInfo")
    node.location = (-1260, -1120)
    node.transform_space = "RELATIVE"
    node.inputs[1].default_value = False
    new_nodes["Object Info"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Exclude by View Dist"
    node.location = (-260, -480)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-260, -960)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-260, -640)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-260, -800)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, -640)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Exclude by View Dist"
    node.location = (-900, -480)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, -800)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-900, -960)
    node.operation = "LENGTH"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-620, -640)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, -640)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshEdgeVertices")
    node.location = (-440, -1720)
    new_nodes["Edge Vertices"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -1580)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -1460)
    node.operation = "NORMALIZE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.008"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-440, -1400)
    new_nodes["Normal.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -960)
    node.operation = "DOT_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -1100)
    node.operation = "CROSS_PRODUCT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (-440, -1240)
    node.input_type = "VECTOR"
    node.inputs[1].default_value = False
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = 0.000000
    node.inputs[4].default_value = 0
    node.inputs[5].default_value = 0
    node.inputs[10].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[11].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    node.inputs[12].default_value = ""
    node.inputs[13].default_value = ""
    new_nodes["Switch"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, -1100)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math.004"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-620, -1240)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Exclude by Angle"
    node.location = (-440, -160)
    node.operation = "ADD"
    node.use_clamp = True
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-440, -800)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-900, 560)
    node.node_tree = bpy.data.node_groups.get(SHELL_ARRAY_GEO_NG_NAME)
    new_nodes["Group"] = node

    node = tree_nodes.new(type="GeometryNodeGroup")
    node.location = (-260, 280)
    node.node_tree = bpy.data.node_groups.get(FRINGE_EXTRUDE_GEO_NG_NAME)
    new_nodes["Group.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1620, -140)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (220, 440)
    new_nodes["Group Output"] = node

    # create links
    tree_links = node_group.links
    tree_links.new(new_nodes["Position.002"].outputs[0], new_nodes["Capture Attribute.002"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[1], new_nodes["Group Output"].inputs[11])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Group.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group"].inputs[6])
    tree_links.new(new_nodes["Group"].outputs[2], new_nodes["Group Output"].inputs[5])
    tree_links.new(new_nodes["Group"].outputs[3], new_nodes["Group Output"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group"].inputs[7])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Group.001"].outputs[1], new_nodes["Group Output"].inputs[8])
    tree_links.new(new_nodes["Capture Attribute"].outputs[2], new_nodes["Group Output"].inputs[7])
    tree_links.new(new_nodes["Join Geometry"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Group.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[21], new_nodes["Group Output"].inputs[12])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Object Info"].inputs[0])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.001"].outputs[0], new_nodes["Vector Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Normal.001"].outputs[0], new_nodes["Vector Math.002"].inputs[1])
    tree_links.new(new_nodes["Group"].outputs[1], new_nodes["Group Output"].inputs[4])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Group"].inputs[8])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Group"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Group.001"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Group"].outputs[0], new_nodes["Join Geometry"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group"].inputs[2])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[16], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Vector Math.004"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Vector Math.005"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.006"].outputs[0], new_nodes["Vector Math.003"].inputs[1])
    tree_links.new(new_nodes["Edge Vertices"].outputs[2], new_nodes["Vector Math.007"].inputs[0])
    tree_links.new(new_nodes["Edge Vertices"].outputs[3], new_nodes["Vector Math.007"].inputs[1])
    tree_links.new(new_nodes["Vector Math.007"].outputs[0], new_nodes["Vector Math.008"].inputs[0])
    tree_links.new(new_nodes["Vector Math.008"].outputs[0], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Group.001"].inputs[6])
    tree_links.new(new_nodes["Normal.002"].outputs[0], new_nodes["Switch"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Switch"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Switch"].inputs[9])
    tree_links.new(new_nodes["Switch"].outputs[3], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Group.001"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Group.001"].inputs[4])
    tree_links.new(new_nodes["Object Info"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Group.001"].inputs[5])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.009"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[17], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math.009"].outputs[1], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[18], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[1], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Vector Math.010"].outputs[1], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Vector Math.004"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[19], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[20], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Group Output"].inputs[10])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Group Output"].inputs[9])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[1], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.026"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Vector Math.003"].outputs[1], new_nodes["Math.007"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

GEO_NODES_MOD_OUTPUT_NAME_STR = [
    "poms_shell_count",
    "poms_min_height",
    "poms_max_height",
    "poms_shell_index",
    "poms_shell_height",
    "poms_shell_offset",
    "poms_fringe",
    "poms_fringe_height",
    "poms_shell_exclude",
    "poms_fringe_exclude",
    "poms_original_pos",
    "uv_map",
]

def create_obj_shell_fringe(ob, override_create, height_mult):
    ensure_node_groups(override_create, [SHELL_ARRAY_GEO_NG_NAME, FRINGE_EXTRUDE_GEO_NG_NAME], 'GeometryNodeTree',
                       create_prereq_shell_fringe_node_group)
    geo_nodes_mod = ob.modifiers.new(name="Shells and Fringe Geometry Nodes", type='NODES')
    if geo_nodes_mod.node_group is None:
        node_group = bpy.data.node_groups.new(name="ShellFringeGeometryNodes", type='GeometryNodeTree')
    else:
        # copy ref to node_group, and remove modifier's ref to node_group, so that default values can be
        # populated
        node_group = geo_nodes_mod.node_group
        geo_nodes_mod.node_group = None
    create_obj_mod_geo_nodes_shell_fringe(node_group)
    # assign node_group to Geometry Nodes modifier, which will populate modifier's default input
    # values from node_group's default input values
    geo_nodes_mod.node_group = node_group

    # set attribute name strings in geometry node modifier outputs - this is cumbersome, because indexing of outputs
    # is not always in sequence - it's unpredictable except for order of outputs in modifier's items collection
    # E.g. output attributes (items) in order may be named 'Output_28_attribute_name', 'Output_20_attribute_name',
    # 'Output_21_attribute_name', ...
    output_count = -1
    for mod_io_item in geo_nodes_mod.items():
        if mod_io_item[0].lower().startswith("output_"):
            output_count = output_count + 1
            # if output_count is too high then gracefully fail
            if output_count >= len(GEO_NODES_MOD_OUTPUT_NAME_STR):
                break    # error
            # assign the string to the output
            geo_nodes_mod[mod_io_item[0]] = GEO_NODES_MOD_OUTPUT_NAME_STR[output_count]

    # set default height multiplier in the modifier inputs - so search for correct input just like when setting outputs
    for mod_io_item in geo_nodes_mod.items():
        if mod_io_item[0].lower() == "input_3":
            geo_nodes_mod[mod_io_item[0]] = -height_mult
            break

class POMSTER_CreateObjModShellFringe(bpy.types.Operator):
    bl_description = "Add geometry nodes modifier to active Mesh object to add Parallax Map Shell and Fringe"
    bl_idname = "pomster.add_object_shell_fringe"
    bl_label = "Shell and Fringe"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object != None and context.active_object.type == 'MESH'

    def execute(self, context):
        scn = context.scene
        create_obj_shell_fringe(context.active_object, scn.POMster.nodes_override_create,
                                scn.POMster.default_height_multiplier)
        return {'FINISHED'}
