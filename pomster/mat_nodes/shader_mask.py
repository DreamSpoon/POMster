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

from .node_other import (ensure_node_group, MAT_NG_NAME_SUFFIX)

CUBE_MASK_MAT_NG_NAME = "CubeMask" + MAT_NG_NAME_SUFFIX
SPHERE_MASK_MAT_NG_NAME = "SphereMask" + MAT_NG_NAME_SUFFIX

def create_prereq_node_group(node_group_name, node_tree_type, custom_data):
    if node_tree_type == 'ShaderNodeTree':
        if node_group_name == CUBE_MASK_MAT_NG_NAME:
            return create_mat_ng_cube_mask()
        elif node_group_name == SPHERE_MASK_MAT_NG_NAME:
            return create_mat_ng_sphere_mask()

    # error
    print("Unknown name passed to create_prereq_node_group: " + str(node_group_name))
    return None

def create_mat_ng_cube_mask():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=CUBE_MASK_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Test Position")
    new_node_group.inputs.new(type='NodeSocketVector', name="Cube Location")
    new_node_group.inputs.new(type='NodeSocketVectorEuler', name="Cube Rotation")
    new_node_group.inputs.new(type='NodeSocketVector', name="Cube Scale")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (-60, -20)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    new_nodes["Map Range"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (300, -100)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    new_nodes["Map Range.002"] = node

    node = tree_nodes.new(type="ShaderNodeMapRange")
    node.location = (120, -60)
    node.clamp = True
    node.data_type = "FLOAT"
    node.interpolation_type = "LINEAR"
    new_nodes["Map Range.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (660, 60)
    node.operation = "DISTANCE"
    new_nodes["Vector Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.location = (480, -20)
    new_nodes["Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -120)
    new_nodes["Separate XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -240)
    new_nodes["Separate XYZ.002"] = node

    node = tree_nodes.new(type="ShaderNodeSeparateXYZ")
    node.location = (-260, -360)
    new_nodes["Separate XYZ.001"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-440, -240)
    node.operation = "MULTIPLY"
    node.inputs[1].default_value = (-1.0, -1.0, -1.0)
    new_nodes["Vector Math.003"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-620, -360)
    node.operation = "DIVIDE"
    node.inputs[1].default_value = (2.0, 2.0, 2.0)
    new_nodes["Vector Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorRotate")
    node.location = (-620, -100)
    node.invert = True
    node.rotation_type = "EULER_XYZ"
    node.inputs[1].default_value = (0.0, 0.0, 0.0)
    new_nodes["Vector Rotate"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-800, -100)
    node.operation = "SUBTRACT"
    node.inputs[2].default_value = (0.0, 0.0, 0.0)
    node.inputs[3].default_value = 1.000000
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1020, -220)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (860, 60)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Vector Math.001"].outputs[1], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Separate XYZ"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[0], new_nodes["Map Range"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[1], new_nodes["Map Range.001"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ"].outputs[2], new_nodes["Map Range.002"].inputs[0])
    tree_links.new(new_nodes["Map Range"].outputs[0], new_nodes["Combine XYZ"].inputs[0])
    tree_links.new(new_nodes["Map Range.001"].outputs[0], new_nodes["Combine XYZ"].inputs[1])
    tree_links.new(new_nodes["Map Range.002"].outputs[0], new_nodes["Combine XYZ"].inputs[2])
    tree_links.new(new_nodes["Vector Rotate"].outputs[0], new_nodes["Vector Math.001"].inputs[0])
    tree_links.new(new_nodes["Combine XYZ"].outputs[0], new_nodes["Vector Math.001"].inputs[1])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Separate XYZ.001"].inputs[0])
    tree_links.new(new_nodes["Vector Math.002"].outputs[0], new_nodes["Vector Math.003"].inputs[0])
    tree_links.new(new_nodes["Vector Math.003"].outputs[0], new_nodes["Separate XYZ.002"].inputs[0])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Map Range"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Map Range"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[0], new_nodes["Map Range"].inputs[3])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[0], new_nodes["Map Range"].inputs[4])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Map Range.001"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Map Range.001"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[1], new_nodes["Map Range.001"].inputs[3])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[1], new_nodes["Map Range.001"].inputs[4])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Map Range.002"].inputs[1])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Map Range.002"].inputs[2])
    tree_links.new(new_nodes["Separate XYZ.002"].outputs[2], new_nodes["Map Range.002"].inputs[3])
    tree_links.new(new_nodes["Separate XYZ.001"].outputs[2], new_nodes["Map Range.002"].inputs[4])
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Rotate"].inputs[4])
    tree_links.new(new_nodes["Vector Math"].outputs[0], new_nodes["Vector Rotate"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[3], new_nodes["Vector Math.002"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_cube_shader_mask_node(node_tree, override_create):
    ensure_node_group(override_create, CUBE_MASK_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes
    for n in tree_nodes: n.select = False

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(CUBE_MASK_MAT_NG_NAME)
    node.inputs[3].default_value = (1.0, 1.0, 1.0)
    # set this node to be active node
    node_tree.nodes.active = node

class POMSTER_AddCubeMask(bpy.types.Operator):
    bl_description = "Add a Cube Shader Mask node, which gives Distance value 0 when inside the cube, or the " \
        "distance from the cube if outside the cube"
    bl_idname = "pomster.create_cube_shader_mask_node"
    bl_label = "Cube Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Cube Shader Mask nodebecause current material doesn't use " +
                        "nodes.  Enable material 'Use Nodes' to continue.")
            return {'CANCELLED'}
        create_cube_shader_mask_node(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_mat_ng_sphere_mask():
    # initialize variables
    new_nodes = {}
    new_node_group = bpy.data.node_groups.new(name=SPHERE_MASK_MAT_NG_NAME, type='ShaderNodeTree')
    new_node_group.inputs.new(type='NodeSocketVector', name="Test Position")
    new_node_group.inputs.new(type='NodeSocketFloat', name="Sphere Radius")
    new_node_group.inputs.new(type='NodeSocketVector', name="Sphere Location")
    new_node_group.outputs.new(type='NodeSocketFloat', name="Distance")
    tree_nodes = new_node_group.nodes
    # delete all nodes
    tree_nodes.clear()

    # create nodes
    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-640, -120)
    node.operation = "SUBTRACT"
    node.use_clamp = False
    new_nodes["Math"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-460, -120)
    node.operation = "GREATER_THAN"
    node.use_clamp = False
    node.inputs[1].default_value = 0.000000
    new_nodes["Math.001"] = node

    node = tree_nodes.new(type="ShaderNodeMath")
    node.location = (-280, -120)
    node.operation = "MULTIPLY"
    node.use_clamp = False
    new_nodes["Math.002"] = node

    node = tree_nodes.new(type="ShaderNodeVectorMath")
    node.location = (-820, -120)
    node.operation = "DISTANCE"
    new_nodes["Vector Math"] = node

    node = tree_nodes.new(type="NodeGroupInput")
    node.location = (-1020, -220)
    new_nodes["Group Input"] = node

    node = tree_nodes.new(type="NodeGroupOutput")
    node.location = (-100, -120)
    new_nodes["Group Output"] = node

    # create links
    tree_links = new_node_group.links
    tree_links.new(new_nodes["Group Input"].outputs[0], new_nodes["Vector Math"].inputs[0])
    tree_links.new(new_nodes["Group Input"].outputs[2], new_nodes["Vector Math"].inputs[1])
    tree_links.new(new_nodes["Group Input"].outputs[1], new_nodes["Math"].inputs[1])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.001"].inputs[0])
    tree_links.new(new_nodes["Math.001"].outputs[0], new_nodes["Math.002"].inputs[0])
    tree_links.new(new_nodes["Math.002"].outputs[0], new_nodes["Group Output"].inputs[0])
    tree_links.new(new_nodes["Math"].outputs[0], new_nodes["Math.002"].inputs[1])
    tree_links.new(new_nodes["Vector Math"].outputs[1], new_nodes["Math"].inputs[0])

    # deselect all new nodes
    for n in new_nodes.values(): n.select = False

    return new_node_group

def create_sphere_shader_mask_node(node_tree, override_create):
    ensure_node_group(override_create, SPHERE_MASK_MAT_NG_NAME, 'ShaderNodeTree', create_prereq_node_group)

    tree_nodes = node_tree.nodes
    # deselect all nodes
    for n in tree_nodes: n.select = False

    node = tree_nodes.new(type="ShaderNodeGroup")
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.node_tree = bpy.data.node_groups.get(SPHERE_MASK_MAT_NG_NAME)
    node.inputs[1].default_value = 1.0
    # set this node to be active node
    node_tree.nodes.active = node

class POMSTER_AddSphereMask(bpy.types.Operator):
    bl_description = "Add a Sphere Shader Mask node, which gives Distance value 0 when inside the sphere, or the " \
        "distance from the sphere if outside the sphere"
    bl_idname = "pomster.create_sphere_shader_mask_node"
    bl_label = "Sphere Mask"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Sphere Shader Mask nodebecause current material doesn't use " +
                        "nodes.  Enable material 'Use Nodes' to continue.")
            return {'CANCELLED'}
        create_sphere_shader_mask_node(context.space_data.edit_tree, scn.POMSTER_NodesOverrideCreate)
        return {'FINISHED'}

def create_mask_obj_loc_rot_scl_nodes(node_tree, input_object):
    tree_nodes = node_tree.nodes
    new_nodes = {}

    # deselect all nodes
    for n in tree_nodes: n.select = False

    # create nodes
    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "Loc_" + input_object.name
    node.location = (node_tree.view_center[0] / 2.5, 140 + (node_tree.view_center[1] / 2.5))
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000
    # set this node to be active node
    node_tree.nodes.active = node

    # add driver to get location X
    drv_loc_x = node.inputs[0].driver_add('default_value').driver
    v_loc_x = drv_loc_x.variables.new()
    v_loc_x.type = 'TRANSFORMS'
    v_loc_x.name = "var"
    v_loc_x.targets[0].id = input_object
    v_loc_x.targets[0].transform_type = 'LOC_X'
    v_loc_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_loc_x.targets[0].data_path = "location.x"
    drv_loc_x.expression = v_loc_x.name
    # add driver to get location Y
    drv_loc_y = node.inputs[1].driver_add('default_value').driver
    v_loc_y = drv_loc_y.variables.new()
    v_loc_y.type = 'TRANSFORMS'
    v_loc_y.name = "var"
    v_loc_y.targets[0].id = input_object
    v_loc_y.targets[0].transform_type = 'LOC_Y'
    v_loc_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_loc_y.targets[0].data_path = "location.y"
    drv_loc_y.expression = v_loc_y.name
    # add driver to get location Z
    drv_loc_z = node.inputs[2].driver_add('default_value').driver
    v_loc_z = drv_loc_z.variables.new()
    v_loc_z.type = 'TRANSFORMS'
    v_loc_z.name = "var"
    v_loc_z.targets[0].id = input_object
    v_loc_z.targets[0].transform_type = 'LOC_Z'
    v_loc_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_loc_z.targets[0].data_path = "location.z"
    drv_loc_z.expression = v_loc_z.name

    new_nodes["Loc_Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "Rot_" + input_object.name
    node.location = (node_tree.view_center[0] / 2.5, node_tree.view_center[1] / 2.5)
    node.inputs[0].default_value = 0.000000
    node.inputs[1].default_value = 0.000000
    node.inputs[2].default_value = 0.000000

    # add driver to get rotation X
    drv_rot_x = node.inputs[0].driver_add('default_value').driver
    v_rot_x = drv_rot_x.variables.new()
    v_rot_x.type = 'TRANSFORMS'
    v_rot_x.name = "var"
    v_rot_x.targets[0].id = input_object
    v_rot_x.targets[0].transform_type = 'ROT_X'
    v_rot_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_rot_x.targets[0].data_path = "rotation.x"
    drv_rot_x.expression = v_rot_x.name
    # add driver to get rotation Y
    drv_rot_y = node.inputs[1].driver_add('default_value').driver
    v_rot_y = drv_rot_y.variables.new()
    v_rot_y.type = 'TRANSFORMS'
    v_rot_y.name = "var"
    v_rot_y.targets[0].id = input_object
    v_rot_y.targets[0].transform_type = 'ROT_Y'
    v_rot_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_rot_y.targets[0].data_path = "rotation.y"
    drv_rot_y.expression = v_rot_y.name
    # add driver to get rotation Z
    drv_rot_z = node.inputs[2].driver_add('default_value').driver
    v_rot_z = drv_rot_z.variables.new()
    v_rot_z.type = 'TRANSFORMS'
    v_rot_z.name = "var"
    v_rot_z.targets[0].id = input_object
    v_rot_z.targets[0].transform_type = 'ROT_Z'
    v_rot_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_rot_z.targets[0].data_path = "rotation.z"
    drv_rot_z.expression = v_rot_z.name

    new_nodes["Rot_Combine XYZ"] = node

    node = tree_nodes.new(type="ShaderNodeCombineXYZ")
    node.label = "Scl_" + input_object.name
    node.location = (node_tree.view_center[0] / 2.5, -140 + (node_tree.view_center[1] / 2.5))
    node.inputs[0].default_value = 1.000000
    node.inputs[1].default_value = 1.000000
    node.inputs[2].default_value = 1.000000

    # add driver to get scale X
    drv_scl_x = node.inputs[0].driver_add('default_value').driver
    v_scl_x = drv_scl_x.variables.new()
    v_scl_x.type = 'TRANSFORMS'
    v_scl_x.name = "var"
    v_scl_x.targets[0].id = input_object
    v_scl_x.targets[0].transform_type = 'SCALE_X'
    v_scl_x.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scl_x.targets[0].data_path = "scale.x"
    drv_scl_x.expression = v_scl_x.name
    # add driver to get scale Y
    drv_scl_y = node.inputs[1].driver_add('default_value').driver
    v_scl_y = drv_scl_y.variables.new()
    v_scl_y.type = 'TRANSFORMS'
    v_scl_y.name = "var"
    v_scl_y.targets[0].id = input_object
    v_scl_y.targets[0].transform_type = 'SCALE_Y'
    v_scl_y.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scl_y.targets[0].data_path = "scale.y"
    drv_scl_y.expression = v_scl_y.name
    # add driver to get scale Z
    drv_scl_z = node.inputs[2].driver_add('default_value').driver
    v_scl_z = drv_scl_z.variables.new()
    v_scl_z.type = 'TRANSFORMS'
    v_scl_z.name = "var"
    v_scl_z.targets[0].id = input_object
    v_scl_z.targets[0].transform_type = 'SCALE_Z'
    v_scl_z.targets[0].transform_space = 'TRANSFORM_SPACE'
    v_scl_z.targets[0].data_path = "scale.z"
    drv_scl_z.expression = v_scl_z.name

    new_nodes["Scl_Combine XYZ"] = node

class POMSTER_AddMaskObjLocRotSclNodes(bpy.types.Operator):
    bl_description = "Add nodes to give object location, rotation, scale - automatically updated (using drivers)"
    bl_idname = "pomster.create_mask_object_loc_rot_scl_nodes"
    bl_label = "Object Loc, Rot, Scl"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        s = context.space_data
        return s.type == 'NODE_EDITOR' and s.node_tree != None and s.tree_type == 'ShaderNodeTree'

    def execute(self, context):
        scn = context.scene
        # check that the material has a nodes tree
        if context.space_data.edit_tree.nodes is None:
            self.report({'ERROR'}, "Unable to create Object Loc, Rot, Scl nodes because current material doesn't " +
                        "use nodes.  Enable material 'Use Nodes' to continue.")
            return {'CANCELLED'}
        if scn.POMSTER_MaskInputObject is None:
            self.report({'ERROR'}, "Unable to create Object Loc, Rot, Scl nodes because Object is blank. Select " +
                        "Object and try again.")
            return {'CANCELLED'}
        create_mask_obj_loc_rot_scl_nodes(context.space_data.edit_tree, scn.POMSTER_MaskInputObject)
        return {'FINISHED'}
