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

from ..node_other import (ensure_node_group, ensure_node_groups, MAT_NG_NAME_SUFFIX)

SHELL_FRINGE_BLEND_MAT_NG_NAME = "ShellFringeBlend" + MAT_NG_NAME_SUFFIX
CUSTOM_SFB_INPUT_MAT_NG_NAME = "CustomSF_Shader" + MAT_NG_NAME_SUFFIX

def create_prereq_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == SHELL_FRINGE_BLEND_MAT_NG_NAME:
            return create_mat_ng_shell_fringe_blend()
        elif node_group_name == CUSTOM_SFB_INPUT_MAT_NG_NAME:
            return create_mat_ng_custom_sfb_input(custom_data)

def create_mat_ng_shell_fringe_blend():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SHELL_FRINGE_BLEND_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.clear()
    new_node_group.outputs.clear()
    new_node_group.inputs.new(type='NodeSocketShader', name="Opaque Shader")
    new_node_group.inputs.new(type='NodeSocketShader', name="Shell / Fringe Shader")
    new_node_group.inputs.new(type='NodeSocketShader', name="Shell Trans Shader")
    new_node_group.inputs.new(type='NodeSocketShader', name="Fringe Trans Shader")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Displacement Height")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Min Height")
    new_input.default_value = -0.020000
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Height")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Shell Index")
    new_input.min_value = 0.000000
    new_node_group.inputs.new(type='NodeSocketFloat', name="Shell Height")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Use Opaque")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    new_input = new_node_group.inputs.new(type='NodeSocketFloatFactor', name="Fringe")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    new_node_group.inputs.new(type='NodeSocketFloat', name="Fringe Height")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Shell Min Alpha Bias")
    new_input.default_value = -0.001000
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Shell Max Alpha Bias")
    new_input.default_value = 0.001000
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Fringe Min Alpha Bias")
    new_input.default_value = -0.001000
    new_node_group.inputs.new(type='NodeSocketFloat', name="Fringe Max Alpha Bias")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Shell Exclude")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Fringe Exclude")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    new_node_group.outputs.new(type='NodeSocketShader', name="Shader")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-320, -420)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.018"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-320, -260)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.017"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-140, -260)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-320, -580)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    new_nodes["Map Range.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-320, -840)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.022"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-940, -800)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[3].default_value = 1.000000
    node.inputs[4].default_value = 0.000000
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -780)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -1120)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -940)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-940, -1060)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.016"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -260)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, -260)
    node.operation = "ADD"
    node.use_clamp = True
    new_nodes["Math.013"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1120, -260)
    node.operation = "LESS_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-940, -260)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.015"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-760, -440)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-940, -440)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-940, -620)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    new_nodes["Math.012"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-560, -600)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "If All Heights = Zero"
    node.location = (-560, -440)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Opaque Bottom Shell"
    node.location = (-1300, -260)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "Use Opaque"
    node.location = (-760, 180)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-960, 180)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, 20)
    node.operation = "ADD"
    node.use_clamp = True
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.label = "Shell with Alpha"
    node.location = (-560, -120)
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-140, -100)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.label = "Fringe with Alpha"
    node.location = (-140, 40)
    new_nodes["Mix Shader.003"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.label = "Blend Opaque w Shell"
    node.location = (-560, 180)
    new_nodes["Mix Shader.001"] = node

    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.label = "Fringe or Opaque/Shell"
    node.location = (-140, 180)
    new_nodes["Mix Shader.002"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1600, -180)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (60, 180)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[10], new_nodes["Mix Shader.002"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Mix Shader"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[9], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[16], new_nodes["Math.006"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Mix Shader.001"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.004"].inputs[1])
    tree_links.new(new_nodes["Mix Shader.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Mix Shader.003"].outputs[0], new_nodes["Mix Shader.002"].inputs[2])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Mix Shader.001"].outputs[0], new_nodes["Mix Shader.002"].inputs[1])
    tree_links.new(new_nodes["Mix Shader"].outputs[0], new_nodes["Mix Shader.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Mix Shader.001"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.009"].inputs[1])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Math.010"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Math.016"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Map Range.001"].inputs[4])
    tree_links.new(new_nodes["Math.012"].outputs[0], new_nodes["Map Range.001"].inputs[3])
    tree_links.new(new_nodes["Math.015"].outputs[0], new_nodes["Math.013"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Math.013"].inputs[1])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Math.015"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Math.011"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.012"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.012"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.016"].inputs[1])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[12], new_nodes["Map Range"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[13], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.016"].inputs[0])
    tree_links.new(new_nodes["Math.013"].outputs[0], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Math.022"].outputs[0], new_nodes["Map Range.003"].inputs[0])
    tree_links.new(new_nodes["Math.017"].outputs[0], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range.003"].outputs[0], new_nodes["Map Range.002"].inputs[4])
    tree_links.new(new_nodes["Math.018"].outputs[0], new_nodes["Map Range.002"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Math.017"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Math.017"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.018"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.018"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Math.022"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[14], new_nodes["Map Range.003"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[15], new_nodes["Map Range.003"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[11], new_nodes["Math.022"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[17], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Mix Shader.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Mix Shader.003"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Mix Shader"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Mix Shader.003"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_shell_fringe_blend_node(node_tree, override_create):
    ensure_node_group(override_create, SHELL_FRINGE_BLEND_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes in tree before creating new node
    for node in tree_nodes: node.select = False

    # create a node group node and give it a ref to the POMster UV nodegroup
    node = tree_nodes.new(type="ShaderNodeGroup")
    view_center = node_tree.view_center
    node.location = (view_center[0] / 1.5, view_center[1] / 1.5)
    node.node_tree = bpy.data.node_groups.get(SHELL_FRINGE_BLEND_MAT_NG_NAME)
    node.select = True
    # make new node the active node
    tree_nodes.active = node

def create_mat_ng_custom_sfb_input(custom_data):
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=CUSTOM_SFB_INPUT_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.clear()
    new_node_group.outputs.clear()
    new_node_group.inputs.new(type='NodeSocketVector', name="UV")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Fringe")
    new_input.min_value = 0.000000
    new_input.max_value = 1.000000
    new_node_group.outputs.new(type='NodeSocketShader', name="Shader")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Height")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeTexImage")
    node.label = "Base Color"
    node.location = (-160, 240)
    node.image = custom_data["base_color_img"]
    new_nodes["Image Texture.005"] = node

    node = tree_nodes.new(type="ShaderNodeTexImage")
    node.label = "Normal"
    node.location = (-160, -300)
    node.image = custom_data["normal_img"]
    new_nodes["Image Texture.004"] = node

    node = tree_nodes.new(type="ShaderNodeTexImage")
    node.label = "Displacement"
    node.location = (-160, -620)
    node.image = custom_data["height_img"]
    new_nodes["Image Texture"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfPrincipled")
    node.location = (240, 240)
    new_nodes["Principled BSDF.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-340, -300)
    node.operation = "SUBTRACT"
    node.use_clamp = True
    node.inputs[0].default_value = 1.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeNormalMap")
    node.location = (-160, -140)
    node.space = "TANGENT"
    node.uv_map = ""
    new_nodes["Normal Map.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-340, -140)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.600000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-660, -180)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (640, 220)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Principled BSDF.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Image Texture.004"].outputs[0], new_nodes["Normal Map.001"].inputs[1])
    tree_links.new(new_nodes["Image Texture.005"].outputs[0], new_nodes["Principled BSDF.002"].inputs[0])
    tree_links.new(new_nodes["Normal Map.001"].outputs[0], new_nodes["Principled BSDF.002"].inputs[22])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Image Texture.005"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Image Texture.004"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Normal Map.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Image Texture"].inputs[0])
    tree_links.new(new_nodes["Image Texture"].outputs[0], new_nodes["Group Output"].inputs[1])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_shell_fringe_blend_and_input_nodes(node_tree, override_create, base_color_img_input, normal_img_input,
                                              height_img_input):
    ensure_node_group(True, CUSTOM_SFB_INPUT_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group,
                      {
                          "base_color_img": base_color_img_input,
                          "normal_img": normal_img_input,
                          "height_img": height_img_input,
                        } )
    ensure_node_group(override_create, SHELL_FRINGE_BLEND_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes in tree before creating new node
    for node in tree_nodes: node.select = False

    new_nodes = {}

    # create nodes
    node = tree_nodes.new(type="NodeFrame")
    node.label = "UV Map"
    node.location = (-460, 460)
    node.label_size = 20
    node.shrink = True
    new_nodes["Frame"] = node

    node = tree_nodes.new(type="ShaderNodeOutputMaterial")
    node.location = (1120, 700)
    node.target = "ALL"
    new_nodes["Material Output"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Shell Height"
    node.location = (480, 300)
    node.attribute_name = "poms_shell_height"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.002"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Shell Index"
    node.location = (260, 300)
    node.attribute_name = "poms_shell_index"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.008"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (480, -240)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.label = "cos View Angle"
    node.location = (480, -100)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.label = "Use Opaque"
    node.location = (480, 120)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "LINEAR"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.85
    elem.color = (0.000000, 0.000000, 0.000000, 1.000000)
    elem = node.color_ramp.elements.new(1.0)
    elem.color = (1.000000, 1.000000, 1.000000, 1.000000)
    new_nodes["ColorRamp.001"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (300, -320)
    new_nodes["Geometry.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorTransform")
    node.location = (300, -100)
    node.convert_from = "CAMERA"
    node.convert_to = "WORLD"
    node.vector_type = "VECTOR"
    node.inputs[0].default_value = (0.0, 0.0, -1.0)
    new_nodes["Vector Transform"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Fringe Height"
    node.location = (260, 120)
    node.attribute_name = "poms_fringe_height"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.007"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Max Height"
    node.location = (260, 480)
    node.attribute_name = "poms_max_height"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.006"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Min Height"
    node.location = (260, 660)
    node.attribute_name = "poms_min_height"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.004"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Shell Exclude"
    node.location = (860, 200)
    node.attribute_name = "poms_shell_exclude"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.013"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Fringe Exclude"
    node.location = (860, 20)
    node.attribute_name = "poms_fringe_exclude"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.014"] = node

    node = tree_nodes.new(type="ShaderNodeBsdfTransparent")
    node.location = (680, 600)
    new_nodes["Transparent BSDF"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.label = "Clamped Height"
    node.location = (480, 660)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.100000
    node.inputs[2].default_value = 0.900000
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.label = "Is Fringe?"
    node.location = (-40, 540)
    node.attribute_name = "poms_fringe"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-443, 660)
    node.operation = "MULTIPLY_ADD"
    new_nodes["Vector Math.010"] = node

    node = tree_nodes.new(type="ShaderNodeAttribute")
    node.location = (-623, 360)
    node.attribute_name = "uv_map"
    node.attribute_type = "GEOMETRY"
    new_nodes["Attribute.018"] = node

    node = tree_nodes.new(type="ShaderNodeUVMap")
    node.location = (-443, 500)
    node.from_instancer = False
    node.uv_map = "UVMap"
    new_nodes["UV Map.005"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-623, 480)
    node.operation = "LENGTH"
    new_nodes["Vector Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-623, 660)
    node.operation = "COMPARE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    new_nodes["Math.014"] = node

    node = tree_nodes.new(type="ShaderNodeMapping")
    node.location = (-260, 660)
    new_nodes["Mapping"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (-40, 700)
    node.node_tree = bpy.data.node_groups.get(CUSTOM_SFB_INPUT_MAT_NG_NAME)
    new_nodes["Group.002"] = node

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (860, 700)
    node.node_tree = bpy.data.node_groups.get(SHELL_FRINGE_BLEND_MAT_NG_NAME)
    new_nodes["Group.004"] = node

    # parenting of nodes
    new_nodes["Vector Math.010"].parent = new_nodes["Frame"]
    new_nodes["Attribute.018"].parent = new_nodes["Frame"]
    new_nodes["UV Map.005"].parent = new_nodes["Frame"]
    new_nodes["Vector Math.009"].parent = new_nodes["Frame"]
    new_nodes["Math.014"].parent = new_nodes["Frame"]
    new_nodes["Mapping"].parent = new_nodes["Frame"]

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Attribute.007"].outputs[2], new_nodes["Group.004"].inputs[11])
    tree_links.new(new_nodes["Attribute.006"].outputs[2], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Attribute.004"].outputs[2], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Group.004"].inputs[4])
    tree_links.new(new_nodes["Vector Transform"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Geometry.001"].outputs[1], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["ColorRamp.001"].inputs[0])
    tree_links.new(new_nodes["ColorRamp.001"].outputs[0], new_nodes["Group.004"].inputs[9])
    tree_links.new(new_nodes["Attribute.013"].outputs[2], new_nodes["Group.004"].inputs[16])
    tree_links.new(new_nodes["Attribute.004"].outputs[2], new_nodes["Group.004"].inputs[5])
    tree_links.new(new_nodes["Group.004"].outputs[0], new_nodes["Material Output"].inputs[0])
    tree_links.new(new_nodes["Attribute.008"].outputs[2], new_nodes["Group.004"].inputs[7])
    tree_links.new(new_nodes["Attribute.006"].outputs[2], new_nodes["Group.004"].inputs[6])
    tree_links.new(new_nodes["Attribute.002"].outputs[2], new_nodes["Group.004"].inputs[8])
    tree_links.new(new_nodes["Attribute.018"].outputs[1], new_nodes["Vector Math.009"].inputs[0])
    tree_links.new(new_nodes["Vector Math.009"].outputs[1], new_nodes["Math.014"].inputs[0])
    tree_links.new(new_nodes["Math.014"].outputs[0], new_nodes["Vector Math.010"].inputs[0])
    tree_links.new(new_nodes["UV Map.005"].outputs[0], new_nodes["Vector Math.010"].inputs[1])
    tree_links.new(new_nodes["Attribute.018"].outputs[1], new_nodes["Vector Math.010"].inputs[2])
    tree_links.new(new_nodes["Attribute.014"].outputs[2], new_nodes["Group.004"].inputs[17])
    tree_links.new(new_nodes["Mapping"].outputs[0], new_nodes["Group.002"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Group.004"].inputs[1])
    tree_links.new(new_nodes["Group.002"].outputs[1], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Attribute.003"].outputs[2], new_nodes["Group.004"].inputs[10])
    tree_links.new(new_nodes["Transparent BSDF"].outputs[0], new_nodes["Group.004"].inputs[2])
    tree_links.new(new_nodes["Transparent BSDF"].outputs[0], new_nodes["Group.004"].inputs[3])
    tree_links.new(new_nodes["Vector Math.010"].outputs[0], new_nodes["Mapping"].inputs[0])
    tree_links.new(new_nodes["Group.002"].outputs[0], new_nodes["Group.004"].inputs[0])
    tree_links.new(new_nodes["Attribute.003"].outputs[2], new_nodes["Group.002"].inputs[1])

    # offset new nodes to view center
    view_center = (node_tree.view_center[0] / 1.5, node_tree.view_center[1] / 1.5)
    for n in new_nodes.values():
        # do not adjust frame location
        if n.type == 'FRAME':
            continue
        n.location = (n.location[0]+view_center[0], n.location[1]+view_center[1])

class POMSTER_AddShellFringeBlendNode(bpy.types.Operator):
    bl_description = "Add a Shell Fringe Blend node to blend between: Opaque with no transparency, Shell " \
        "with horizontal (U, V, Height) transparency, and Fringe with vertical (U, V, Height) transparency"
    bl_idname = "pomster.create_shell_fringe_blend_node"
    bl_label = "Shell Fringe Blend"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Shell Fringe Blend node because current material doesn't " +
                        "use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        # if inputs are needed then create input nodes, otherwise create only Shell Fringe Blend node
        if scn.POMster.add_shell_fringe_inputs:
            create_shell_fringe_blend_and_input_nodes(context.space_data.edit_tree, scn.POMster.nodes_override_create,
                scn.POMster.base_color_img_input, scn.POMster.normal_img_input, scn.POMster.height_img_input)
        else:
            create_shell_fringe_blend_node(context.space_data.edit_tree, scn.POMster.nodes_override_create)
        return {'FINISHED'}
