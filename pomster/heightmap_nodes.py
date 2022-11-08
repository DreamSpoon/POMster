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

# material (shader) node group names
POMSTER_UV_MAT_NG_NAME = "POMsterUV.MatNG.POMSTER"

#BEGIN_JITTER3_MAT_NG_NAME = "BeginJitter3.MatNG.POMSTER"
#WEIGHT_JITTER3_MAT_NG_NAME = "WeightJitter3.POMSTER.MatNG"

#DENOISE1_MAT_NG_NAME = "Denoise1.POMSTER.MatNG"

# node names
#BEGIN_JITTER_HEIGHTMAP_000_NODENAME = "HeightmapJitter.000"
#BEGIN_JITTER_HEIGHTMAP_001_NODENAME = "HeightmapJitter.001"
#BEGIN_JITTER_HEIGHTMAP_002_NODENAME = "HeightmapJitter.002"

JITTER_POM_GROUP_000_GRP_NODENAME = "JitterPOM_Group.000"
JITTER_POM_GROUP_001_GRP_NODENAME = "JitterPOM_Group.001"
JITTER_POM_GROUP_002_GRP_NODENAME = "JitterPOM_Group.002"

#BEGIN_JITTER_GRP_NODENAME = "JitterGroup"
#JITTER_POM_GRP_NODENAME = "JitterPOM_CombineGroup"

HEIGHTMAP_ORIGINAL_NODENAME = "Heightmap.Original"

#WEIGHT_JITTER_GRP_NODENAME = "JitterWeightGroup"

#HEIGHTMAP_DENOISE_000_NODENAME = "HeightmapDenoise.000"

#DENOISE_WEIGHT_000_GRP_NODENAME = "DenoiseWeight1Group"

#DENOISE_POM_000_GRP_NODENAME = "DenoisePOM1Group"

U_TANGENT_NODENAME = "Tangent U Map"
V_TANGENT_NODENAME = "Tangent V Map"
ASPECT_RATIO_NODENAME = "Aspect Ratio"
TEXTURE_COORD_NODENAME = "UV Texture Coordinate"

#WEIGHTED_HEIGHT_OF_JITTER_NODENAME = "WHJitter.Math"

#WEIGHTED_HEIGHT_OF_DENOISE_000_NODENAME = "WHDenoise000.Math"

SPREAD_SAMPLE3_MAT_NG_NAME = "SpreadSample3.MatNG.POMSTER"
ERROR_SIGN_BIAS3_MAT_NG_NAME = "ErrorSignBias3.MatNG.POMSTER"
HEIGHT_ERROR_CUTOFF3_MAT_NG_NAME = "HeightErrorCutoff3.MatNG.POMSTER"
COMBINE_SAMPLE3_MAT_NG_NAME = "CombineSample3.MatNG.POMSTER"
BIAS_CUTOFF_COMBINE3_MAT_NG_NAME = "BiasCutoffCombine3.MatNG.POMSTER"
SHARPEN_POM_MAT_NG_NAME = "SharpenPOM.MatNG.POMSTER"

def create_prereq_util_node_group(node_group_name, node_tree_type):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == POMSTER_UV_MAT_NG_NAME:
            return create_mat_ng_pomster()
#        elif node_group_name == BEGIN_JITTER3_MAT_NG_NAME:
#            return create_mat_ng_begin_jitter3()
#        elif node_group_name == WEIGHT_JITTER3_MAT_NG_NAME:
#            return create_mat_ng_weight_jitter3()
#        elif node_group_name == DENOISE1_MAT_NG_NAME:
#            return create_mat_ng_denoise1()
        elif node_group_name == SPREAD_SAMPLE3_MAT_NG_NAME:
            return create_mat_ng_spread_sample3()
        elif node_group_name == ERROR_SIGN_BIAS3_MAT_NG_NAME:
            return create_mat_ng_error_sign_bias3()
        elif node_group_name == HEIGHT_ERROR_CUTOFF3_MAT_NG_NAME:
            return create_mat_ng_height_error_cutoff3()
        elif node_group_name == COMBINE_SAMPLE3_MAT_NG_NAME:
            return create_mat_ng_combine_sample3()
        elif node_group_name == BIAS_CUTOFF_COMBINE3_MAT_NG_NAME:
            return create_mat_ng_bias_cutoff_combine3()
        elif node_group_name == SHARPEN_POM_MAT_NG_NAME:
            return create_mat_ng_sharpen_pom()

    # error
    print("Unknown name passed to create_prereq_util_node_group: " + str(node_group_name))
    return None

# done
def create_mat_ng_pomster():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=POMSTER_UV_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Height")
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

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (-600, -200)
    new_nodes["Geometry"] = node

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
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math.006"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Vector Math.003"].inputs[3])
    tree_links.new(new_nodes["Vector Math.006"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Vector Math.004"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Combine XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Combine XYZ.001"].inputs[1])
    tree_links.new(new_nodes["Combine XYZ.001"].outputs[0], new_nodes["Vector Math.004"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math.006"].inputs[1])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math.005"].inputs[1])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math.005"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

# done
def create_mat_ng_spread_sample3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SPREAD_SAMPLE3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Center")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Radius")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample 1")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample 2")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample 3")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, 80)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-240, -80)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-460, -40)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-20, -40)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

# done
def create_mat_ng_error_sign_bias3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=ERROR_SIGN_BIAS3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="High Bias Factor")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 3")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Error 1")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Error 2")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Error 3")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, 180)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, 0)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, -180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-360, 0)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-540, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 180)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[1].default_value = 3.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[1].default_value = 3.000000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (0, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 0)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (400, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (400, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (180, 180)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1120, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (580, 20)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.010"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

# done
def create_mat_ng_height_error_cutoff3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=HEIGHT_ERROR_CUTOFF3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Error 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Error 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Error 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff 3")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Cutoff 1")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Cutoff 2")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Sample Cutoff 3")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Average Error"
    node.location = (-720, 440)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 280)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, 120)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1080, 120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-720, 280)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, 440)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1620, 440)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Ensure > 0"
    node.location = (-1440, 440)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, 440)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (280, 280)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.034"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (460, 280)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.035"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Ensure > 0"
    node.location = (640, 280)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.036"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (820, 280)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.037"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 440)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 440)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 280)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 280)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-400, 120)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-220, 120)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Weight 2"
    node.location = (-40, 280)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Weight 1"
    node.location = (-40, 440)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Weight 3"
    node.location = (-40, 120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1000, -220)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1000, -60)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (820, -220)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -60)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["Math.027"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, -220)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["Math.029"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1180, 100)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    new_nodes["Math.025"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -60)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.028"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, -220)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.030"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (1360, 100)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.026"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Average Height"
    node.location = (1000, 100)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Height 3"
    node.location = (1540, -220)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.033"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (640, -220)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Height 1"
    node.location = (1540, 100)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.031"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Cutoff Sample Height 2"
    node.location = (1540, -60)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.032"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (820, -60)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2060, 160)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (1760, 100)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.014"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.019"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.020"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.021"].inputs[1])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.024"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.025"].outputs[0], new_nodes["Math.026"].inputs[1])
    tree_links.new(new_nodes["Math.026"].outputs[0], new_nodes["Math.031"].inputs[0])
    tree_links.new(new_nodes["Math.027"].outputs[0], new_nodes["Math.028"].inputs[1])
    tree_links.new(new_nodes["Math.028"].outputs[0], new_nodes["Math.032"].inputs[0])
    tree_links.new(new_nodes["Math.029"].outputs[0], new_nodes["Math.030"].inputs[1])
    tree_links.new(new_nodes["Math.030"].outputs[0], new_nodes["Math.033"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.025"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.027"].inputs[1])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.029"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.031"].inputs[1])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.032"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.033"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.025"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.027"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.029"].inputs[0])
    tree_links.new(new_nodes["Math.034"].outputs[0], new_nodes["Math.035"].inputs[0])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.036"].inputs[0])
    tree_links.new(new_nodes["Math.036"].outputs[0], new_nodes["Math.037"].inputs[0])
    tree_links.new(new_nodes["Math.035"].outputs[0], new_nodes["Math.037"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.034"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.034"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.035"].inputs[1])
    tree_links.new(new_nodes["Math.037"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Math.031"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math.032"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Math.033"].outputs[0], new_nodes["Group Output"].inputs[2])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

# done
def create_mat_ng_combine_sample3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=COMBINE_SAMPLE3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Cutoff 3")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2160, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False

    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1980, 0)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, 0)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2160, -200)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1980, -200)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, -200)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-2160, -400)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1980, -400)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1800, -400)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1620, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1620, -200)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.019"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1620, -400)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.020"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1440, -400)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1440, 0)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1440, -200)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, -200)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Weighted Height"
    node.location = (-1260, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1260, -400)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1080, -200)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Total Weight"
    node.location = (-1080, -0)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Not Equal 0"
    node.location = (-680, 0)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-500, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.024"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-500, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math.023"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Equal 0"
    node.location = (-680, -180)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.021"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-320, 0)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-900, 0)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-2400, 0)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Math.019"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.020"].outputs[0], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.015"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Math.005"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Math.011"].inputs[2])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math.003"].inputs[2])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.019"].inputs[1])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.020"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.021"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Math.023"].inputs[0])
    tree_links.new(new_nodes["Math.021"].outputs[0], new_nodes["Math.024"].inputs[0])
    tree_links.new(new_nodes["Math.024"].outputs[0], new_nodes["Math.023"].inputs[2])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.023"].inputs[1])
    tree_links.new(new_nodes["Math.023"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Math.024"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

# done
def create_mat_ng_bias_cutoff_combine3():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=BIAS_CUTOFF_COMBINE3_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketFloat', name="High Bias Factor")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 1")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 2")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Next 3")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sample Prev 3")
    new_node_group.outputs.new(type='NodeSocketVector', name="UV Output")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Height")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "ErrorSignBias3Grp"
    node.location = (-270, 0)
    node.node_tree = bpy.data.node_groups.get(ERROR_SIGN_BIAS3_MAT_NG_NAME)
    new_nodes["ErrorSignBias3Grp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "HeightErrorCutoff3Grp"
    node.location = (-90, 0)
    node.node_tree = bpy.data.node_groups.get(HEIGHT_ERROR_CUTOFF3_MAT_NG_NAME)
    node.inputs[2].default_value = 1.000000
    node.inputs[5].default_value = 1.000000
    node.inputs[8].default_value = 1.000000
    new_nodes["HeightErrorCutoff3Grp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "CombineSamples3Grp"
    node.location = (90, 0)
    node.node_tree = bpy.data.node_groups.get(COMBINE_SAMPLE3_MAT_NG_NAME)
    new_nodes["CombineSamples3Grp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "CombinedSamplePOMGrp"
    node.location = (270, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes["CombinedSamplePOMGrp"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-460, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (460, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["ErrorSignBias3Grp"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["ErrorSignBias3Grp"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["ErrorSignBias3Grp"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["ErrorSignBias3Grp"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["CombinedSamplePOMGrp"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["CombinedSamplePOMGrp"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["CombinedSamplePOMGrp"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["CombinedSamplePOMGrp"].inputs[2])
    tree_links.new(new_nodes["CombinedSamplePOMGrp"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["ErrorSignBias3Grp"].inputs[0])
    tree_links.new(new_nodes["CombineSamples3Grp"].outputs[0], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["ErrorSignBias3Grp"].outputs[0], new_nodes["HeightErrorCutoff3Grp"].inputs[1])
    tree_links.new(new_nodes["ErrorSignBias3Grp"].outputs[1], new_nodes["HeightErrorCutoff3Grp"].inputs[4])
    tree_links.new(new_nodes["ErrorSignBias3Grp"].outputs[2], new_nodes["HeightErrorCutoff3Grp"].inputs[7])
    tree_links.new(new_nodes["HeightErrorCutoff3Grp"].outputs[0], new_nodes["CombineSamples3Grp"].inputs[2])
    tree_links.new(new_nodes["HeightErrorCutoff3Grp"].outputs[1], new_nodes["CombineSamples3Grp"].inputs[5])
    tree_links.new(new_nodes["HeightErrorCutoff3Grp"].outputs[2], new_nodes["CombineSamples3Grp"].inputs[8])
    tree_links.new(new_nodes["CombineSamples3Grp"].outputs[0], new_nodes["CombinedSamplePOMGrp"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["HeightErrorCutoff3Grp"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["CombineSamples3Grp"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["HeightErrorCutoff3Grp"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["CombineSamples3Grp"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["ErrorSignBias3Grp"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["ErrorSignBias3Grp"].inputs[5])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["HeightErrorCutoff3Grp"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["CombineSamples3Grp"].inputs[6])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["CombineSamples3Grp"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["CombineSamples3Grp"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["CombineSamples3Grp"].inputs[7])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

# done
def create_mat_ng_sharpen_pom():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SHARPEN_POM_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="UV Input")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent U Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Tangent V Map")
    new_node_group.inputs.new(type='NodeSocketVector', name="Aspect Ratio")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Next Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Prev Height")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sharpen Factor")
    new_node_group.outputs.new(type='NodeSocketVector', name="UV Output")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Height")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (0, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes["Group.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -180)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, -340)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-180, 0)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-360, 0)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (190, 0)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Group.018"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Group.018"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Group.018"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Group.018"].inputs[2])
    tree_links.new(new_nodes["Group.018"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Math"].inputs[2])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group.018"].inputs[4])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Group Output"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_inputs_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, user_input_index):
    node = tree_nodes.new(type="ShaderNodeTexCoord")
    node.location = (-1020, 0)
    node.from_instancer = False
    new_nodes[TEXTURE_COORD_NODENAME] = node
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
    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = "U Tangent"
    node.location = (-1020, -260)
    node.direction_type = "UV_MAP"
    new_nodes[U_TANGENT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeTangent")
    node.label = "V Tangent"
    node.location = (-1020, -360)
    node.direction_type = "UV_MAP"
    new_nodes[V_TANGENT_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "Aspect Ratio"
    node.location = (-1020, -460)
    node.inputs[0].default_value = 1.0
    node.inputs[1].default_value = 1.0
    node.inputs[2].default_value = 1.0
    new_nodes[ASPECT_RATIO_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "High Bias Factor"
    node.location = (-1020, -600)
    node.outputs[0].default_value = 1.000000
    new_nodes["High Bias Factor"] = node

    node = tree_nodes.new(type="ShaderNodeValue")
    node.label = "Sharpen Factor"
    node.location = (-1020, -700)
    node.outputs[0].default_value = 0.500000
    new_nodes["Sharpen Factor"] = node

    return [ input_uv_link_socket, output_to_sockets ]

def create_spread_sample3_nodes_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, user_input_index):
    # create nodes
#    node = tree_nodes.new(type="ShaderNodeGroup")
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.label = "Sample1HeightmapGrp"
    node.location = (-780, 240)
#    node.node_tree = bpy.data.node_groups.get("NodeGroup")
    new_nodes["Sample1HeightmapGrp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "Sample1POMGrp"
    node.location = (-780, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes["Sample1POMGrp"] = node

#    node = tree_nodes.new(type="ShaderNodeGroup")
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.label = "Sample2HeightmapGrp"
    node.location = (-780, -220)
#    node.node_tree = bpy.data.node_groups.get("NodeGroup")
    new_nodes["Sample2HeightmapGrp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "Sample2POMGrp"
    node.location = (-780, -440)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes["Sample2POMGrp"] = node

#    node = tree_nodes.new(type="ShaderNodeGroup")
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.label = "Sample3HeightmapGrp"
    node.location = (-780, -640)
#    node.node_tree = bpy.data.node_groups.get("NodeGroup")
    new_nodes["Sample3HeightmapGrp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "Sample3POMGrp"
    node.location = (-780, -860)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes["Sample3POMGrp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "SpreadSample3Grp"
    node.location = (-780, -1080)
    node.node_tree = bpy.data.node_groups.get(SPREAD_SAMPLE3_MAT_NG_NAME)
    node.inputs[0].default_value = -0.050000
    node.inputs[1].default_value = 0.050000
    new_nodes["SpreadSample3Grp"] = node

    # create links
    tree_links.new(new_nodes["SpreadSample3Grp"].outputs[0], new_nodes["Sample1POMGrp"].inputs[2])
    tree_links.new(new_nodes["SpreadSample3Grp"].outputs[1], new_nodes["Sample2POMGrp"].inputs[2])
    tree_links.new(new_nodes["SpreadSample3Grp"].outputs[2], new_nodes["Sample3POMGrp"].inputs[2])
    tree_links.new(new_nodes["Sample1POMGrp"].outputs[0], new_nodes["Sample1HeightmapGrp"].inputs[0])
    tree_links.new(new_nodes["Sample2POMGrp"].outputs[0], new_nodes["Sample2HeightmapGrp"].inputs[0])
    tree_links.new(new_nodes["Sample3POMGrp"].outputs[0], new_nodes["Sample3HeightmapGrp"].inputs[0])

def create_sharpen_pom_row(tree_nodes, tree_links, new_nodes, user_heightmap_node):
    # create nodes
#    node = tree_nodes.new(type="ShaderNodeGroup")
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.label = "CombinedSampleHeightmapGrp"
    node.location = (-340, 0)
#    node.node_tree = bpy.data.node_groups.get("NodeGroup")
    new_nodes["CombinedSampleHeightmapGrp"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "SharpenPOMGrp"
    node.location = (0, 0)
    node.node_tree = bpy.data.node_groups.get(SHARPEN_POM_MAT_NG_NAME)
    new_nodes["SharpenPOMGrp"] = node

    # create links
    tree_links.new(new_nodes["CombinedSampleHeightmapGrp"].outputs[0], new_nodes["SharpenPOMGrp"].inputs[4])


# TODO delete this function
def create_begin_jitter3_nodes_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, input_uv_link_socket,
                               user_input_index, user_output_index):
    # create nodes
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-740, 330)
    new_nodes[BEGIN_JITTER_HEIGHTMAP_000_NODENAME] = node

    running_y_offset = -user_heightmap_node.dimensions[1] / 2.5

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-740, 310+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-740, 80+running_y_offset)
    new_nodes[BEGIN_JITTER_HEIGHTMAP_001_NODENAME] = node

    running_y_offset = running_y_offset - user_heightmap_node.dimensions[1] / 2.5

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-740, 60+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME] = node

    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-740, -170+running_y_offset)
    new_nodes[BEGIN_JITTER_HEIGHTMAP_002_NODENAME] = node

    running_y_offset = running_y_offset - user_heightmap_node.dimensions[1] / 2.5

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-740, -190+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-740, -420+running_y_offset)
    node.node_tree = bpy.data.node_groups.get(BEGIN_JITTER3_MAT_NG_NAME)
    node.inputs[1].default_value = 0.1
    node.inputs[2].default_value = 0.0
    new_nodes[BEGIN_JITTER_GRP_NODENAME] = node

    node = user_heightmap_node
    node.location = (-740, -620+running_y_offset)
    new_nodes[HEIGHTMAP_ORIGINAL_NODENAME] = node

    # create links
    tree_links.new(new_nodes[BEGIN_JITTER_GRP_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].inputs[2])
    tree_links.new(new_nodes[BEGIN_JITTER_GRP_NODENAME].outputs[1], new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].inputs[2])
    tree_links.new(new_nodes[BEGIN_JITTER_GRP_NODENAME].outputs[2], new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].inputs[2])
    tree_links.new(new_nodes[ASPECT_RATIO_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].inputs[1])
    tree_links.new(new_nodes[ASPECT_RATIO_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].inputs[1])
    tree_links.new(new_nodes[ASPECT_RATIO_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].inputs[1])
    tree_links.new(input_uv_link_socket, new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].inputs[0])
    tree_links.new(input_uv_link_socket, new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].inputs[0])
    tree_links.new(input_uv_link_socket, new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].inputs[0])
    tree_links.new(new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].outputs[0], new_nodes[BEGIN_JITTER_HEIGHTMAP_000_NODENAME].inputs[user_input_index])
    tree_links.new(new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].outputs[0], new_nodes[BEGIN_JITTER_HEIGHTMAP_001_NODENAME].inputs[user_input_index])
    tree_links.new(new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].outputs[0], new_nodes[BEGIN_JITTER_HEIGHTMAP_002_NODENAME].inputs[user_input_index])
    tree_links.new(new_nodes[HEIGHTMAP_ORIGINAL_NODENAME].outputs[user_output_index], new_nodes[BEGIN_JITTER_GRP_NODENAME].inputs[0])
    tree_links.new(new_nodes[U_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].inputs[3])
    tree_links.new(new_nodes[U_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].inputs[3])
    tree_links.new(new_nodes[U_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].inputs[3])
    tree_links.new(new_nodes[V_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].inputs[4])
    tree_links.new(new_nodes[V_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].inputs[4])
    tree_links.new(new_nodes[V_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].inputs[4])
    tree_links.new(new_nodes[TEXTURE_COORD_NODENAME].outputs[1], new_nodes[JITTER_POM_GROUP_000_GRP_NODENAME].inputs[5])
    tree_links.new(new_nodes[TEXTURE_COORD_NODENAME].outputs[1], new_nodes[JITTER_POM_GROUP_001_GRP_NODENAME].inputs[5])
    tree_links.new(new_nodes[TEXTURE_COORD_NODENAME].outputs[1], new_nodes[JITTER_POM_GROUP_002_GRP_NODENAME].inputs[5])

# TODO delete this function
def create_weight_jitter3_nodes_column(tree_nodes, tree_links, new_nodes, input_uv_link_socket, user_output_index):
    # create nodes
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-460, -390)
    node.node_tree = bpy.data.node_groups.get(WEIGHT_JITTER3_MAT_NG_NAME)
    node.inputs[6].default_value = 1
    node.inputs[7].default_value = -1
    new_nodes[WEIGHT_JITTER_GRP_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-460, -220)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes[WEIGHTED_HEIGHT_OF_JITTER_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-460, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes[JITTER_POM_GRP_NODENAME] = node

    # create links
    tree_links.new(new_nodes[BEGIN_JITTER_HEIGHTMAP_000_NODENAME].outputs[user_output_index], new_nodes[WEIGHT_JITTER_GRP_NODENAME].inputs[0])
    tree_links.new(new_nodes[BEGIN_JITTER_HEIGHTMAP_001_NODENAME].outputs[user_output_index], new_nodes[WEIGHT_JITTER_GRP_NODENAME].inputs[2])
    tree_links.new(new_nodes[BEGIN_JITTER_HEIGHTMAP_002_NODENAME].outputs[user_output_index], new_nodes[WEIGHT_JITTER_GRP_NODENAME].inputs[4])
    tree_links.new(new_nodes[BEGIN_JITTER_GRP_NODENAME].outputs[2], new_nodes[WEIGHT_JITTER_GRP_NODENAME].inputs[5])
    tree_links.new(new_nodes[BEGIN_JITTER_GRP_NODENAME].outputs[1], new_nodes[WEIGHT_JITTER_GRP_NODENAME].inputs[3])
    tree_links.new(new_nodes[BEGIN_JITTER_GRP_NODENAME].outputs[0], new_nodes[WEIGHT_JITTER_GRP_NODENAME].inputs[1])
    tree_links.new(new_nodes[WEIGHT_JITTER_GRP_NODENAME].outputs[1], new_nodes[WEIGHTED_HEIGHT_OF_JITTER_NODENAME].inputs[1])
    tree_links.new(new_nodes[WEIGHT_JITTER_GRP_NODENAME].outputs[0], new_nodes[WEIGHTED_HEIGHT_OF_JITTER_NODENAME].inputs[0])
    tree_links.new(input_uv_link_socket, new_nodes[JITTER_POM_GRP_NODENAME].inputs[0])
    tree_links.new(new_nodes[ASPECT_RATIO_NODENAME].outputs[0], new_nodes[JITTER_POM_GRP_NODENAME].inputs[1])
    tree_links.new(new_nodes[U_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GRP_NODENAME].inputs[3])
    tree_links.new(new_nodes[V_TANGENT_NODENAME].outputs[0], new_nodes[JITTER_POM_GRP_NODENAME].inputs[4])
    tree_links.new(new_nodes[WEIGHTED_HEIGHT_OF_JITTER_NODENAME].outputs[0], new_nodes[JITTER_POM_GRP_NODENAME].inputs[2])
    tree_links.new(new_nodes[TEXTURE_COORD_NODENAME].outputs[1], new_nodes[JITTER_POM_GRP_NODENAME].inputs[5])

# TODO delete this function
def create_denoise1_nodes_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, input_uv_link_socket,
                                 user_input_index, user_output_index):
    # create nodes
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (-280, -890)
    new_nodes[HEIGHTMAP_DENOISE_000_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-280, -700)
    node.node_tree = bpy.data.node_groups.get(DENOISE1_MAT_NG_NAME)
    new_nodes[DENOISE_WEIGHT_000_GRP_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, -540)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["DenoiseMath.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, -380)
    node.operation = "ADD"
    node.use_clamp = False
    new_nodes["DenoiseMath.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, -220)
    node.operation = "DIVIDE"
    node.use_clamp = False
    new_nodes[WEIGHTED_HEIGHT_OF_DENOISE_000_NODENAME] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-280, 0)
    node.node_tree = bpy.data.node_groups.get(POMSTER_UV_MAT_NG_NAME)
    new_nodes[DENOISE_POM_000_GRP_NODENAME] = node

    # create links
    tree_links.new(new_nodes[JITTER_POM_GRP_NODENAME].outputs[0], new_nodes[HEIGHTMAP_DENOISE_000_NODENAME].inputs[user_input_index])
    tree_links.new(new_nodes[HEIGHTMAP_DENOISE_000_NODENAME].outputs[user_output_index], new_nodes[DENOISE_WEIGHT_000_GRP_NODENAME].inputs[0])
    tree_links.new(new_nodes[WEIGHTED_HEIGHT_OF_JITTER_NODENAME].outputs[0], new_nodes[DENOISE_WEIGHT_000_GRP_NODENAME].inputs[1])
    tree_links.new(new_nodes[DENOISE_WEIGHT_000_GRP_NODENAME].outputs[1], new_nodes["DenoiseMath.002"].inputs[1])
    tree_links.new(new_nodes[WEIGHT_JITTER_GRP_NODENAME].outputs[1], new_nodes["DenoiseMath.002"].inputs[0])
    tree_links.new(input_uv_link_socket, new_nodes[HEIGHTMAP_ORIGINAL_NODENAME].inputs[user_input_index])
    tree_links.new(new_nodes[DENOISE_WEIGHT_000_GRP_NODENAME].outputs[0], new_nodes["DenoiseMath.001"].inputs[1])
    tree_links.new(new_nodes[WEIGHT_JITTER_GRP_NODENAME].outputs[0], new_nodes["DenoiseMath.001"].inputs[0])
    tree_links.new(new_nodes["DenoiseMath.001"].outputs[0], new_nodes[WEIGHTED_HEIGHT_OF_DENOISE_000_NODENAME].inputs[0])
    tree_links.new(new_nodes["DenoiseMath.002"].outputs[0], new_nodes[WEIGHTED_HEIGHT_OF_DENOISE_000_NODENAME].inputs[1])
    tree_links.new(input_uv_link_socket, new_nodes[DENOISE_POM_000_GRP_NODENAME].inputs[0])
    tree_links.new(new_nodes[ASPECT_RATIO_NODENAME].outputs[0], new_nodes[DENOISE_POM_000_GRP_NODENAME].inputs[1])
    tree_links.new(new_nodes[U_TANGENT_NODENAME].outputs[0], new_nodes[DENOISE_POM_000_GRP_NODENAME].inputs[3])
    tree_links.new(new_nodes[V_TANGENT_NODENAME].outputs[0], new_nodes[DENOISE_POM_000_GRP_NODENAME].inputs[4])
    tree_links.new(new_nodes[WEIGHTED_HEIGHT_OF_DENOISE_000_NODENAME].outputs[0], new_nodes[DENOISE_POM_000_GRP_NODENAME].inputs[2])
    tree_links.new(new_nodes[TEXTURE_COORD_NODENAME].outputs[1], new_nodes[DENOISE_POM_000_GRP_NODENAME].inputs[5])


def create_heightmap_apply_nodes(tree_nodes, tree_links, user_heightmap_node, user_input_index, user_output_index):
    # initialize variables
    new_nodes = {}

    nodes_offset = (user_heightmap_node.location[0], user_heightmap_node.location[1])

    # create inputs column
    input_uv_link_socket, output_to_sockets = create_inputs_column(tree_nodes, tree_links, new_nodes,
                                                                   user_heightmap_node, user_input_index)
    # create spread sample column and link it to the inputs column
    create_spread_sample3_nodes_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, user_input_index)
    link_input_column_to_sample_column(tree_links, new_nodes)

    # bias, cutoff, and combine group node
    node = tree_nodes.new(type="ShaderNodeGroup")
    node.label = "BiasCutoffCombine3Grp"
    node.location = (-520, 0)
    node.node_tree = bpy.data.node_groups.get(BIAS_CUTOFF_COMBINE3_MAT_NG_NAME)
    new_nodes["BiasCutoffCombine3Grp"] = node
    # link inputs to above node
    link_input_column_to_bcc_grp_node(tree_links, new_nodes)

    # sharpen row and input links
    create_sharpen_pom_row(tree_nodes, tree_links, new_nodes, user_heightmap_node)
    link_input_column_to_sharpen_row(tree_links, new_nodes)

    link_sample_column_to_bias_cutoff_combine_node(tree_links, new_nodes)
    link_bias_cutoff_combine_node_to_sharpen_row(tree_links, new_nodes)
    link_sample_column_to_bias_cutoff_combine_node(tree_links, new_nodes)

#    # create bias cutoff combine row and link it to the inputs column
#    create_bias_cutoff_combine3_row(tree_nodes, tree_links, new_nodes)
#    link_input_column_to_bias_cutoff_combine3_row(tree_links, new_nodes)

#    # create sharpen POM row and link it to the inputs column
#    create_sharpen_pom_row(tree_nodes, tree_links, new_nodes)
#    link_input_column_to_sharpen_pom_row(tree_links, new_nodes)

#    # more links
#    link_sample_column_to_bias_cutoff_combine3_row(tree_links, new_nodes)
#    link_bias_cutoff_combine_row_to_sharpen_row(tree_links, new_nodes)

#    OLD
#    create_begin_jitter3_nodes_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, input_uv_link_socket,
#                                     user_input_index, user_output_index)
#    create_weight_jitter3_nodes_column(tree_nodes, tree_links, new_nodes, input_uv_link_socket, user_output_index)
#    create_denoise1_nodes_column(tree_nodes, tree_links, new_nodes, user_heightmap_node, input_uv_link_socket,
#                                 user_input_index, user_output_index)
#    OLD

    # create final node, a duplicate that appears to be in the same place as the originally selected node
    node = duplicate_user_node(tree_nodes, user_heightmap_node)
    node.location = (0, 0)
    new_nodes["Heightmap.Final"] = node

    # fix output links to re-create original user node's output links, but use calculated height
#    relink_final_user_node(tree_links, new_nodes["Heightmap.Final"], new_nodes[SHARPEN_POM_000_GRP_NODENAME].outputs[0],
#                           output_to_sockets, user_input_index)

    # deselect and offset all new nodes
    for n in new_nodes.values():
        n.select = False
        n.location[0] = n.location[0] + nodes_offset[0]
        n.location[1] = n.location[1] + nodes_offset[1]

    return new_nodes

def link_input_column_to_sample_column(tree_links, new_nodes):
    # create links
    tree_links.new(new_nodes["UV Texture Coordinate"].outputs[2], new_nodes["Sample1POMGrp"].inputs[0])
    tree_links.new(new_nodes["Aspect Ratio"].outputs[0], new_nodes["Sample1POMGrp"].inputs[3])
    tree_links.new(new_nodes["Aspect Ratio"].outputs[0], new_nodes["Sample2POMGrp"].inputs[3])
    tree_links.new(new_nodes["Aspect Ratio"].outputs[0], new_nodes["Sample3POMGrp"].inputs[3])
    tree_links.new(new_nodes["UV Texture Coordinate"].outputs[2], new_nodes["Sample2POMGrp"].inputs[0])
    tree_links.new(new_nodes["UV Texture Coordinate"].outputs[2], new_nodes["Sample3POMGrp"].inputs[0])
    tree_links.new(new_nodes["Tangent U Map"].outputs[0], new_nodes["Sample1POMGrp"].inputs[1])
    tree_links.new(new_nodes["Tangent U Map"].outputs[0], new_nodes["Sample2POMGrp"].inputs[1])
    tree_links.new(new_nodes["Tangent U Map"].outputs[0], new_nodes["Sample3POMGrp"].inputs[1])
    tree_links.new(new_nodes["Tangent V Map"].outputs[0], new_nodes["Sample1POMGrp"].inputs[2])
    tree_links.new(new_nodes["Tangent V Map"].outputs[0], new_nodes["Sample2POMGrp"].inputs[2])
    tree_links.new(new_nodes["Tangent V Map"].outputs[0], new_nodes["Sample3POMGrp"].inputs[2])

def link_input_column_to_bcc_grp_node(tree_links, new_nodes):
    # create links
    tree_links.new(new_nodes["UV Texture Coordinate"].outputs[2], new_nodes["BiasCutoffCombine3Grp"].inputs[0])
    tree_links.new(new_nodes["Aspect Ratio"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[3])
    tree_links.new(new_nodes["Tangent U Map"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[1])
    tree_links.new(new_nodes["Tangent V Map"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[2])
    tree_links.new(new_nodes["High Bias Factor"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[4])

def link_input_column_to_sharpen_row(tree_links, new_nodes):
    # create links
    tree_links.new(new_nodes["UV Texture Coordinate"].outputs[2], new_nodes["SharpenPOMGrp"].inputs[0])
    tree_links.new(new_nodes["Aspect Ratio"].outputs[0], new_nodes["SharpenPOMGrp"].inputs[3])
    tree_links.new(new_nodes["Tangent U Map"].outputs[0], new_nodes["SharpenPOMGrp"].inputs[1])
    tree_links.new(new_nodes["Tangent V Map"].outputs[0], new_nodes["SharpenPOMGrp"].inputs[2])
    tree_links.new(new_nodes["Sharpen Factor"].outputs[0], new_nodes["SharpenPOMGrp"].inputs[6])

def link_sample_column_to_bias_cutoff_combine_node(tree_links, new_nodes):
    # create links
    tree_links.new(new_nodes["Sample1HeightmapGrp"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[5])
    tree_links.new(new_nodes["Sample3HeightmapGrp"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[9])
    tree_links.new(new_nodes["SpreadSample3Grp"].outputs[2], new_nodes["BiasCutoffCombine3Grp"].inputs[10])
    tree_links.new(new_nodes["SpreadSample3Grp"].outputs[1], new_nodes["BiasCutoffCombine3Grp"].inputs[8])
    tree_links.new(new_nodes["SpreadSample3Grp"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[6])
    tree_links.new(new_nodes["Sample2HeightmapGrp"].outputs[0], new_nodes["BiasCutoffCombine3Grp"].inputs[7])

def link_bias_cutoff_combine_node_to_sharpen_row(tree_links, new_nodes):
    # create links
    tree_links.new(new_nodes["BiasCutoffCombine3Grp"].outputs[0], new_nodes["CombinedSampleHeightmapGrp"].inputs[0])
    tree_links.new(new_nodes["CombinedSampleHeightmapGrp"].outputs[0], new_nodes["SharpenPOMGrp"].inputs[4])
    tree_links.new(new_nodes["BiasCutoffCombine3Grp"].outputs[1], new_nodes["SharpenPOMGrp"].inputs[5])

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
                       [POMSTER_UV_MAT_NG_NAME,
#                        BEGIN_JITTER3_MAT_NG_NAME,
#                        WEIGHT_JITTER3_MAT_NG_NAME,
#                        DENOISE1_MAT_NG_NAME,
                         SPREAD_SAMPLE3_MAT_NG_NAME,
                         ERROR_SIGN_BIAS3_MAT_NG_NAME,
                         HEIGHT_ERROR_CUTOFF3_MAT_NG_NAME,
                         COMBINE_SAMPLE3_MAT_NG_NAME,
                         BIAS_CUTOFF_COMBINE3_MAT_NG_NAME,
                         SHARPEN_POM_MAT_NG_NAME,
                        ],
                       'ShaderNodeTree', create_prereq_util_node_group)

    create_heightmap_apply_nodes(node_tree.nodes, node_tree.links, user_heightmap_node, user_input_index,
                                 user_output_index)

class POMSTER_AddPOMsterToSelectedNode(bpy.types.Operator):
    bl_description = "Using selected node as a basis, add nodes to create a Parallax Occlusion Map (POM) effect to " \
        "the material. Selected node must have at least one vector input and at least one value output"
    bl_idname = "pomster.create_pom_uv"
    bl_label = "POMster UV"
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
