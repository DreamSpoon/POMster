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

def create_util_ortho_tangents(node_tree):
    offset = (node_tree.view_center[0]/2.5, node_tree.view_center[1]/2.5)

    # initialize
    new_nodes = {}
    tree_nodes = node_tree.nodes

    # create nodes
    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Tangent V"
    node.location = (180+offset[0], -200+offset[1])
    node.operation = "CROSS_PRODUCT"
    node.inputs[1].default_value = (1.0, 0.0, 0.0)
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.label = "Tangent U"
    node.location = (180+offset[0], 0+offset[1])
    node.operation = "CROSS_PRODUCT"
    node.inputs[1].default_value = (0.0, -1.0, 0.0)
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (0+offset[0], 0+offset[1])
    new_nodes["Geometry"] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math.001"].inputs[0])

class POMSTER_AddUtilOrthoTangents(bpy.types.Operator):
    bl_description = "Add nodes to get U and V tangents based on XY orthographic texture projection. Use this to " \
        "get procedural U and V tangents for e.g. landscape / terrain"
    bl_idname = "pomster.create_util_orthographic_tangents_nodes"
    bl_label = "XY Ortho Tangents"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility XY Orthographic Tangents nodes because current " +
                        "material doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_util_ortho_tangents(context.space_data.edit_tree)
        return {'FINISHED'}

def create_util_optimum_distance(node_tree):
    offset = (node_tree.view_center[0]/2.5, node_tree.view_center[1]/2.5)

    # initialize
    new_nodes = {}
    tree_nodes = node_tree.nodes

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMixShader")
    node.location = (offset[0], offset[1])
    new_nodes["Mix Shader"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (offset[0], offset[1]-140)
    node.operation = "MULTIPLY_ADD"
    node.use_clamp = True
    node.inputs[1].default_value = 0.03
    node.inputs[2].default_value = -0.03
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeLightPath")
    node.location = (offset[0], offset[1]-320)
    new_nodes["Light Path"] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Mix Shader"].inputs[0])
    tree_links.new(new_nodes["Light Path"].outputs[7], new_nodes["Math"].inputs[0])

class POMSTER_AddUtilOptimumDistance(bpy.types.Operator):
    bl_description = "Add nodes to help reduce render times (Cycles only) by optimizing use of POM by distance " \
        "- farther areas do not have POM effect applied. Mix Shader's first input is OCPOM shader branch, " \
        "second input is 'flat' shader branch"
    bl_idname = "pomster.create_util_optimum_distance_nodes"
    bl_label = "Optimum Distance"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Optimum Distance nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_util_optimum_distance(context.space_data.edit_tree)
        return {'FINISHED'}

def create_util_depth_angle_fix(node_tree):
    tree_nodes = node_tree.nodes
    new_nodes = {}
    offset = (node_tree.view_center[0]/2.5, node_tree.view_center[1]/2.5)

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (offset[0], offset[1])
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeValToRGB")
    node.location = (offset[0], offset[1]-160)
    node.color_ramp.color_mode = "RGB"
    node.color_ramp.interpolation = "B_SPLINE"
    node.color_ramp.elements.remove(node.color_ramp.elements[0])
    elem = node.color_ramp.elements[0]
    elem.position = 0.2
    elem.color = (0, 0, 0, 1)
    elem = node.color_ramp.elements.new(0.5)
    elem.color = (1, 1, 1, 1)
    new_nodes["ColorRamp"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (offset[0], offset[1]-380)
    node.operation = "DOT_PRODUCT"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="ShaderNodeNewGeometry")
    node.location = (offset[0], offset[1]-520)
    new_nodes["Geometry"] = node

    # create links
    tree_links = node_tree.links
    tree_links.new(new_nodes["Geometry"].outputs[1], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Geometry"].outputs[4], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["ColorRamp"].inputs[0])
    tree_links.new(new_nodes["ColorRamp"].outputs[0], new_nodes["Math"].inputs[1])

class POMSTER_DepthAngleFix(bpy.types.Operator):
    bl_description = "Add nodes to fix the warping effect that appears as viewing angle approaches perpendicular " \
        "to the face normal. Multiply by depth value (displacement value) of the texture"
    bl_idname = "pomster.create_util_depth_angle_fix_nodes"
    bl_label = "Depth Angle Fix"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create utility Depth Angle Fix nodes because current material " +
                        "doesn't use nodes. Enable material 'Use Nodes' to continue")
            return {'CANCELLED'}
        create_util_depth_angle_fix(context.space_data.edit_tree)
        return {'FINISHED'}
