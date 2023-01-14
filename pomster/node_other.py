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

MAT_NG_NAME_SUFFIX = ".POMS"

def ensure_node_group(override_create, node_group_name, node_tree_type, create_group_func, custom_data=None):
    # check if custom node group already exists, and create/override if necessary
    node_group = bpy.data.node_groups.get(node_group_name)
    if node_group is None or node_group.type != node_tree_type or override_create:
        # create the custom node group
        node_group = create_group_func(node_group_name, node_tree_type, custom_data)
        if node_group is None:
            return None
        # if override create is enabled, then ensure new group name will be "first", meaning:
        #     group name does not have suffix like '.001', '.002', etc.
        if override_create:
            node_group.name = node_group_name
    return node_group

def ensure_node_groups(override_create, ng_name_list, node_tree_type, create_group_func, custom_data=None):
    for ng_name in ng_name_list:
        ensure_node_group(override_create, ng_name, node_tree_type, create_group_func, custom_data)

def get_node_group_for_type(ng_type):
    if ng_type in ['CompositorNodeTree', 'ShaderNodeTree', 'TextureNodeTree']:
        return 'ShaderNodeGroup'
    elif ng_type == 'GeometryNodeTree':
        return 'GeometryNodeGroup'
    return None

# get the UVMap to be used as either tangent U or tangent V,
# with tangent_type = either "U" or "V"
def get_tangent_map_name(tangent_type, active_obj):
    if active_obj is None:
        return ""
    # check all UV layers (UV maps) by name for either:
    #     a '(U, V) Map' to use as Tangent U vector, or
    #     a '(V, U) Map' to use as Tangent V vector
    # else:
    #     return error # graceful fail
    for uv_layer in active_obj.data.uv_layers:
        if (uv_layer.name.lower().startswith("uvmap") and tangent_type == "U") or \
            (uv_layer.name.lower().startswith("vumap") and tangent_type == "V"): return uv_layer.name
    # graceful fail will not cause errors later, return error
    return ""
