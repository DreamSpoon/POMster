# POMster
Parallax Occlusion Map (POM) addon for Blender
Create the effect of millions of geometry faces with only one face, using a parallax depth effect combined with occlusion culling.
Ray tracing inside a material, to complement ray-tracing outside the material.

# Material Shader Parallax Mapping
A simple Parallax Map node can be added to a material to give the effect of a depth to a flat material.
An OCPOM node can be added to to a material to give the effect of depth to a bumpy material.

# Geometry Nodes Shell and Fringe with Parallax mapping

# Utility
There are some utility node creation buttons to help use Parallax Mapping / OCPOM:
1) XY Orthographic Tangents
  - creates nodes to use as input Tangent U, Tangent V
  - gives correct tangents for use with height displaced geometry, e.g. landscapes, procedural geometry

The OCPOM effect uses many more texture samples than a "flat" texture (only one sample), so the POM effect increases render times as a result. More samples equals longer render times. The addon comes with some utility nodes to help reduce render times by using POM only when it makes a difference.
  - near geometry should use POM, but far geometry does not benefit as much from POM
  - incoming light rays that are not directly visible to the camera don't need POM
    - e.g. sahdow rays can use the "flat" texture
  - Cycles shaders can be optimized with the Mix Shader node
The following utility nodes can be used in EEVEE or Cycles, but any reduction in render times only applies to Cycles, and only with the Mix Shader node. This is because of the way that Blender optimizes shader node trees for rendering. This optimization applies to the Mix Shader node only (the node that has two Shader inputs), and not the Mix Color node. See Blender Cycles Node Optimizations resource for more information.
2) Optimum Type
  - only these ray types are (potentially) directly visible to the camera:
    - Camera Ray
	- Transparent Ray
	- Reflection Ray
	- Glossy (maybe redundant to include Glossy, as Reflection might be enough)
3) Optimum Length
  - creates a Mix Shader node setup that will reduce render times by removing the OCPOM effect from far geometry
	- the OCPOM effect is slower to render than 'flat' materials, because it requires more samples of input textures to create the effect
	- Parallax Map effect is not noticeable after a certain distance, about 100 meters - depending on maximum depth used in Parallax Map
	- reduce render times by using OCPOM effect only on near geometry, given that OCPOM effect is not noticeable on far geometry
  - how to use:
    - connect OCPOM final shader node to first Shader input of Mix Shader
    - connect 'flat' final shader node to second Shader input of Mix Shader
  - important note!
    - OCPOM shader nodes set and 'flat' shader nodes set must not have any nodes in common - zero shared nodes/links!
      - this optimization only works if the two 'branches' (OCPOM branch and 'flat' branch) of the mix shader are completely separate
	  - here is what the Blender documentation has to say about the subject:
	    - 'When executing shaders, a special optimization is applied to Mix Shader nodes. If Factor evaluates to 0 or 1, any nodes that are only reachable via the unused branch of the mix are not evaluated.'
4) Optimum Angle (helps fix texture warp in some cases)
  - OCPOM effect looks warped as the viewing angle becomes extreme (i.e. view angle almost parallel to face)
  - this group node fixes the problem by reducing the OCPOM effect as the angle becomes extreme
  - to use this node, multiply its output with the depth value (displacement) from the depth texture map (displacement texture map)
  - using the node will cause the texture to look flat (no POM effect) when view rays are close to parallel with geometry
5) Combined Optimum
  - use this function to get a quick Mix Shader setup that combines all three of the above Optimum nodes

# Offset Conestep Parallax Occlusion Mapping (OCPOM)
The addon's material shader node groups use Conestep Parallax Occlusion Mapping with a modification: Cone Offset
Cones are Offset "upwards" so that cone steps can be much wider (very "relaxed" cones), and allow the "viewer ray" to travel farther with fewer samples.
For great explanations of Cone Stepping and Parallax mapping, see these resources at bottom of this text:
  - Parallax Mapping at LearnOpenGL
  - Relaxed Cone Stepping Relief Mapping at NVidia

# Parallax Mapping Resources
Parallax Mapping at LearnOpenGL
https://learnopengl.com/Advanced-Lighting/Parallax-Mapping

Relaxed Cone Stepping Relief Mapping at NVidia
https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-18-relaxed-cone-stepping-relief-mapping

Relief Texture Mapping at University of North Carolina at Chapel Hill
https://www.inf.ufrgs.br/~oliveira/pubs_files/RTM.pdf

Blender Cycles Node Optimizations
https://docs.blender.org/manual/en/latest/render/cycles/optimizations/nodes.html
