# POMster - Material Shader Nodes

## Usage
Usage is demonstrated with examples:
1. Plane mesh with Parallax Map node

TODO 2. Plane mesh with Offset Conestep Parallax Occlusion Map (OCPOM) node

### Example 1: Parallax Map node
This example is a plane with Parallax Map material shader nodes applied to give a 'flat' depth effect.

1. Create Plane, including UV map
3DView -> Add menu -> Mesh -> Plane
(docs/assets/mat_shader_nodes/parallax_map/create_plane.png)

2. Create VU Map from UV Map
Create VU Map automatically from the default UV Map with the Flip UV panel.
The VU Map is needed for V Tangent of texture coordinates, for use with Parallax Map node.
If UV Map is not available then other sources of Tangent U/V might be available, e.g. see "Ortho Tangents" button in the POMster node editor panel.

3DView -> Tools -> POMster -> Flip UV
(docs/assets/mat_shader_nodes/parallax_map/flip_uv.png)

3. Create Parallax Map for UV Coordinates
Go to the Shader Editor, and create an Image Texture node with Texture Coordinate node for UV input.
The example uses a Coast Sand texture that can be downloaded from PolyHaven.com - although any texture can be used.
(docs/assets/mat_shader_nodes/parallax_map/before_parallax_map.png)

Delete Texture Coordinate node, then add Parallax Map node and connect to texture node.

Shader Editor -> Tools -> POMster -> Parallax Map -> Parallax Map
(docs/assets/mat_shader_nodes/parallax_map/after_parallax_map.png)

The UV Map and VU Map were automatically selected (based on default names "UVMap" and "VUMap.UVMap") for the U Tangent and V Tangent nodes.
If the UV Map and VU Map have names different from "UVMap" and "VUMap.UVMap", then these values will need to be filled in manually.
(docs/assets/mat_shader_nodes/parallax_map/parallax_map_uv_vu_map_names.png)

With the ParallaxMap.POMS node selected, change the Height value from 0.0 to -0.1

This will make the image texture appear to be inside the geometry, instead of flat at the geometry's surface.
Note: The parallax effect only works with negative Height values. Depth is negative Height, to be consistent when Height is used elsewhere in POMster.
(docs/assets/mat_shader_nodes/parallax_map/change_height_0.1.png)

4. Complete
Comparing old material with new material, the new material's texture looks like it's inside the geometry.
The effect is is more noticable at edges, and at red-white Cursor at world origin.
(docs/assets/mat_shader_nodes/parallax_map/before_parallax_render.png)

(docs/assets/mat_shader_nodes/parallax_map/after_parallax_render.png)
