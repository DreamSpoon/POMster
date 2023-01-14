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

from ..node_other import (ensure_node_group, MAT_NG_NAME_SUFFIX)

SHELL_ARRAY_GEO_NG_NAME = "ShellArray" + MAT_NG_NAME_SUFFIX
FRINGE_EXTRUDE_GEO_NG_NAME = "FringeExtrude" + MAT_NG_NAME_SUFFIX

def create_prereq_shell_fringe_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'GeometryNodeTree':
        if node_group_name == SHELL_ARRAY_GEO_NG_NAME:
            return create_geo_ng_shell_array()
        elif node_group_name == FRINGE_EXTRUDE_GEO_NG_NAME:
            return create_geo_ng_fringe_extrude()

def create_geo_ng_shell_array():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SHELL_ARRAY_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.clear()
    new_node_group.outputs.clear()
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Geometry")
    new_input = new_node_group.inputs.new(type='NodeSocketInt', name="Shell Count")
    new_input.min_value = 2
    new_input.default_value = 4
    new_node_group.inputs.new(type='NodeSocketBool', name="Delete Zero Index")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Min Height")
    new_input.default_value = -0.020000
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Height")
    new_node_group.inputs.new(type='NodeSocketBool', name="Use Other Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Other Normal")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Max Stretch Factor")
    new_input.min_value = 0.000000
    new_input.default_value = 1.000000
    new_node_group.inputs.new(type='NodeSocketBool', name="Shell Exclude")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_output = new_node_group.outputs.new(type='NodeSocketInt', name="Shell Index")
    new_output.min_value = 0
    new_node_group.outputs.new(type='NodeSocketFloat', name="Shell Height")
    new_node_group.outputs.new(type='NodeSocketVector', name="Shell Offset")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, -220)
    node.operation = "MAXIMUM"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-760, -380)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.010"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (-280, 200)
    node.domain = "FACE"
    node.mode = "ALL"
    new_nodes["Delete Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, -120)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, 40)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (-40, 200)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-40, 40)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Index"
    node.location = (180, 200)
    node.data_type = "INT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Height"
    node.location = (380, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Offset"
    node.location = (580, 100)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="GeometryNodeGeometryToInstance")
    node.location = (-1180, -200)
    new_nodes["Geometry to Instance"] = node

    node = tree_nodes.new(type="GeometryNodeRealizeInstances")
    node.location = (-1180, 60)
    node.legacy_behavior = False
    new_nodes["Realize Instances"] = node

    node = tree_nodes.new(type="GeometryNodeDuplicateElements")
    node.location = (-1180, -20)
    node.domain = "INSTANCE"
    new_nodes["Duplicate Elements"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-1380, -140)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-980, 40)
    node.operation = "ADD"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.011"] = node

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-40, -260)
    new_nodes["Normal"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (-40, -100)
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

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.label = "Shell Height"
    node.location = (-760, 40)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, 200)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, 40)
    node.operation = "MINIMUM"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, -120)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, -260)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, -420)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-520, -560)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshEdgeAngle")
    node.location = (-1180, -500)
    new_nodes["Edge Angle"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Edge  Angle"
    node.location = (-1180, -300)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1600, -260)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (780, 160)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Geometry to Instance"].outputs[0], new_nodes["Duplicate Elements"].inputs[0])
    tree_links.new(new_nodes["Duplicate Elements"].outputs[0], new_nodes["Realize Instances"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Vector Math"].inputs[3])
    tree_links.new(new_nodes["Capture Attribute"].outputs[5], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[2], new_nodes["Group Output"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[1], new_nodes["Group Output"].inputs[3])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Capture Attribute.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Switch"].inputs[0])
    tree_links.new(new_nodes["Normal"].outputs[0], new_nodes["Switch"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Switch"].inputs[9])
    tree_links.new(new_nodes["Switch"].outputs[3], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Edge Angle"].outputs[0], new_nodes["Capture Attribute.003"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Geometry to Instance"].inputs[0])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[7], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Math.003"].outputs[0], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Capture Attribute.001"].inputs[2])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Realize Instances"].outputs[0], new_nodes["Delete Geometry"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Capture Attribute"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Capture Attribute"].inputs[5])
    tree_links.new(new_nodes["Math.011"].outputs[0], new_nodes["Math"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Delete Geometry"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[8], new_nodes["Math.001"].inputs[1])
    tree_links.new(new_nodes["Math.010"].outputs[0], new_nodes["Math.003"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.010"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Duplicate Elements"].inputs[2])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Math.011"].inputs[1])
    tree_links.new(new_nodes["Duplicate Elements"].outputs[1], new_nodes["Math.011"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_shell_array_node(node_tree, override_create):
    ensure_node_group(override_create, SHELL_ARRAY_GEO_NG_NAME, 'GeometryNodeTree',
                      create_prereq_shell_fringe_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes in tree before creating new node
    for node in tree_nodes: node.select = False

    # create a node group node
    node = tree_nodes.new(type="GeometryNodeGroup")
    view_center = node_tree.view_center
    node.location = (view_center[0] / 2.5, view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(SHELL_ARRAY_GEO_NG_NAME)

    node.select = True
    # make new node the active node
    tree_nodes.active = node

class POMSTER_AddShellArrayNode(bpy.types.Operator):
    bl_description = "Add a Shell Array node, to make multiple 'shell' copies of input geometry, with shells " \
        "spaced apart evenly - displaced along vertex normals by default, or Other Normals if desired"
    bl_idname = "pomster.create_shell_array_node"
    bl_label = "Shell Array"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that editor nodes tree exists
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Shell Array node because current edit tree doesn't exist")
            return {'CANCELLED'}
        create_shell_array_node(context.space_data.edit_tree, scn.POMster.nodes_override_create)
        return {'FINISHED'}

def create_geo_ng_fringe_extrude():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=FRINGE_EXTRUDE_GEO_NG_NAME, type='GeometryNodeTree')
    new_node_group.inputs.clear()
    new_node_group.outputs.clear()
    new_node_group.inputs.new(type='NodeSocketGeometry', name="Mesh")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Min Height")
    new_input.default_value = -0.020000
    new_node_group.inputs.new(type='NodeSocketFloat', name="Max Height")
    new_node_group.inputs.new(type='NodeSocketBool', name="Use Other Normal")
    new_node_group.inputs.new(type='NodeSocketVector', name="Other Normal")
    new_input = new_node_group.inputs.new(type='NodeSocketFloat', name="Max Stretch Factor")
    new_input.min_value = 0.000000
    new_input.default_value = 4.000000
    new_node_group.inputs.new(type='NodeSocketBool', name="Fringe Exclude")
    new_node_group.outputs.new(type='NodeSocketGeometry', name="Geometry")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Height")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="FunctionNodeBooleanMath")
    node.location = (-140, -20)
    node.operation = "NOT"
    node.inputs[1].default_value = False
    new_nodes["Boolean Math"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (-140, 140)
    node.domain = "FACE"
    node.mode = "ALL"
    new_nodes["Delete Geometry"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (60, -20)
    node.operation = "SCALE"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="GeometryNodeSetPosition")
    node.location = (60, 140)
    new_nodes["Set Position"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Height"
    node.location = (260, 140)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.002"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (460, 140)
    new_nodes["Group Output"] = node

    node = tree_nodes.new(type="GeometryNodeExtrudeMesh")
    node.location = (-340, 60)
    node.mode = "EDGES"
    node.inputs[3].default_value = 0.010000
    node.inputs[4].default_value = True
    new_nodes["Extrude Mesh"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Orig Normal"
    node.location = (-540, -100)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.001"] = node

    node = tree_nodes.new(type="GeometryNodeDeleteGeometry")
    node.location = (-540, 60)
    node.domain = "POINT"
    node.mode = "ALL"
    new_nodes["Delete Geometry.001"] = node

    node = tree_nodes.new(type="GeometryNodeSwitch")
    node.location = (-540, -300)
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

    node = tree_nodes.new(type="GeometryNodeInputNormal")
    node.location = (-540, -460)
    new_nodes["Normal.001"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Orig Position"
    node.location = (-540, -520)
    node.data_type = "FLOAT_VECTOR"
    node.domain = "POINT"
    node.inputs[2].default_value = 0.000000
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-720, -640)
    new_nodes["Position"] = node

    node = tree_nodes.new(type="GeometryNodeCaptureAttribute")
    node.label = "Capture Edge Angle"
    node.location = (-540, -720)
    node.data_type = "FLOAT"
    node.domain = "POINT"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[4].default_value = False
    node.inputs[5].default_value = 0
    new_nodes["Capture Attribute.003"] = node

    node = tree_nodes.new(type="GeometryNodeInputMeshEdgeAngle")
    node.location = (-720, -840)
    new_nodes["Edge Angle"] = node

    node = tree_nodes.new(type="FunctionNodeCompare")
    node.location = (-340, -260)
    node.data_type = "VECTOR"
    node.mode = "ELEMENT"
    node.operation = "EQUAL"
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0
    node.inputs[3].default_value = 0
    node.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
    node.inputs[8].default_value = ""
    node.inputs[9].default_value = ""
    node.inputs[10].default_value = 0.900000
    node.inputs[11].default_value = 0.087266
    node.inputs[12].default_value = 0.000000
    new_nodes["Compare"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-140, -160)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 1.000000
    node.inputs[5].default_value = 4.000000
    node.inputs[7].default_value = (0.0, 0.0, 0.0)
    node.inputs[8].default_value = (1.0, 1.0, 1.0)
    node.inputs[9].default_value = (0.0, 0.0, 0.0)
    node.inputs[10].default_value = (1.0, 1.0, 1.0)
    node.inputs[11].default_value = (4.0, 4.0, 4.0)
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -480)
    node.operation = "ABSOLUTE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.005"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -320)
    node.operation = "MINIMUM"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.007"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -160)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.008"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -920)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.009"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -780)
    node.operation = "COSINE"
    node.use_clamp = False
    node.inputs[1].default_value = 0.500000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.004"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (60, -620)
    node.operation = "DIVIDE"
    node.use_clamp = False
    node.inputs[0].default_value = 1.000000
    node.inputs[2].default_value = 0.500000
    new_nodes["Math.006"] = node

    node = tree_nodes.new(type="GeometryNodeInputPosition")
    node.location = (-340, -480)
    new_nodes["Position.001"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-800, -280)
    new_nodes["Group Input"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry.001"].outputs[0], new_nodes["Extrude Mesh"].inputs[0])
    tree_links.new(new_nodes["Extrude Mesh"].outputs[0], new_nodes["Delete Geometry"].inputs[0])
    tree_links.new(new_nodes["Boolean Math"].outputs[0], new_nodes["Delete Geometry"].inputs[1])
    tree_links.new(new_nodes["Extrude Mesh"].outputs[2], new_nodes["Boolean Math"].inputs[0])
    tree_links.new(new_nodes["Position"].outputs[0], new_nodes["Capture Attribute"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute"].outputs[0], new_nodes["Capture Attribute.001"].inputs[0])
    tree_links.new(new_nodes["Delete Geometry"].outputs[0], new_nodes["Set Position"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute"].outputs[1], new_nodes["Set Position"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Set Position"].inputs[3])
    tree_links.new(new_nodes["Capture Attribute"].outputs[1], new_nodes["Compare"].inputs[4])
    tree_links.new(new_nodes["Position.001"].outputs[0], new_nodes["Compare"].inputs[5])
    tree_links.new(new_nodes["Compare"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Set Position"].outputs[0], new_nodes["Capture Attribute.002"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Capture Attribute.002"].inputs[2])
    tree_links.new(new_nodes["Capture Attribute.002"].outputs[2], new_nodes["Group Output"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.001"].outputs[0], new_nodes["Delete Geometry.001"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[6], new_nodes["Delete Geometry.001"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Normal.001"].outputs[0], new_nodes["Switch"].inputs[8])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Switch"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[4], new_nodes["Switch"].inputs[9])
    tree_links.new(new_nodes["Switch"].outputs[3], new_nodes["Capture Attribute.001"].inputs[1])
    tree_links.new(new_nodes["Edge Angle"].outputs[0], new_nodes["Capture Attribute.003"].inputs[2])
    tree_links.new(new_nodes["Math.004"].outputs[0], new_nodes["Math.006"].inputs[1])
    tree_links.new(new_nodes["Math.006"].outputs[0], new_nodes["Math.005"].inputs[0])
    tree_links.new(new_nodes["Math.005"].outputs[0], new_nodes["Math.007"].inputs[0])
    tree_links.new(new_nodes["Math.007"].outputs[0], new_nodes["Math.008"].inputs[1])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[2], new_nodes["Math.009"].inputs[0])
    tree_links.new(new_nodes["Math.009"].outputs[0], new_nodes["Math.004"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[5], new_nodes["Math.007"].inputs[1])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Math.008"].inputs[0])
    tree_links.new(new_nodes["Math.008"].outputs[0], new_nodes["Vector Math"].inputs[3])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Capture Attribute.003"].inputs[0])
    tree_links.new(new_nodes["Capture Attribute.003"].outputs[0], new_nodes["Capture Attribute"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_fringe_extrude_node(node_tree, override_create):
    ensure_node_group(override_create, FRINGE_EXTRUDE_GEO_NG_NAME, 'GeometryNodeTree',
                      create_prereq_shell_fringe_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes in tree before creating new node
    for node in tree_nodes: node.select = False

    # create a node group node
    node = tree_nodes.new(type="GeometryNodeGroup")
    view_center = node_tree.view_center
    node.location = (view_center[0] / 2.5, view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(FRINGE_EXTRUDE_GEO_NG_NAME)

    node.select = True
    # make new node the active node
    tree_nodes.active = node

class POMSTER_AddFringeExtrudeNode(bpy.types.Operator):
    bl_description = "Add a Fringe Extrude node, to extrude input geometry edges only - extruded along vertex " \
        "normals by default, or Other Normals if desired"
    bl_idname = "pomster.create_fringe_extrude_node"
    bl_label = "Fringe Extrude"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'GeometryNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that editor nodes tree exists
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Fringe Extrude node because current edit tree doesn't exist")
            return {'CANCELLED'}
        create_fringe_extrude_node(context.space_data.edit_tree, scn.POMster.nodes_override_create)
        return {'FINISHED'}
