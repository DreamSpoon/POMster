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
from .node_other import MAT_NG_NAME_SUFFIX

PARALLAX_MAP_MAT_NG_NAME = "ParallaxMap" + MAT_NG_NAME_SUFFIX

def create_mat_ng_pomster():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=PARALLAX_MAP_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V")
    new_node_group.inputs.new(type='NodeSocketVector', name="Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Incoming")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Depth")
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
    node.inputs[0].default_value = 1.000000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, -140)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-220, -280)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-400, 200)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (-220, 200)
    node.inputs[2].default_value = 1.000000
    new_nodes["Combine XYZ.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-600, 80)
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
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Vector Math.004"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Vector Math"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group
