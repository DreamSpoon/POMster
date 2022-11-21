# POMster
Parallax Occlusion Map addon for Blender
Create the effect of extra geometry completely inside a material, using a 'depth' effect combined with occlusion mapping.

# Summary
Use Conestep Parallax Occlusion Mapping with a modification: Cone Offset
Cones are Offset "upwards" so that cone steps can be much wider (very "relaxed" cones), and allow the "viewer ray" to travel further with fewer samples.
Great explanations can be found in resources:
  - Parallax Mapping at LearnOpenGL
  - Relaxed Cone Stepping Relief Mapping at NVidia

# Utility
There are some utility node creation buttons to help use Parallax Mapping / OCPOM:
1) XY Orthographic Tangents
  - creates nodes to use as input Tangent U, Tangent V
  - gives correct tangents for use with height displaced geometry, e.g. landscapes, procedural geometry
2) Optimum Distance (Cycles only)
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
3) Depth Angle Fix
  - OCPOM effect looks warped as the viewing angle becomes extreme (i.e. view angle almost parallel to face)
  - this node set fixes the problem by reducing the OCPOM effect as the angle becomes extreme
  - reduce depth value to zero by multiplying the depth value with the angle factor
  - use the Math Multiply node to multiply with the depth from depth texture map
  - it may be possible to combine this with Optimum Distance node set, to further reduce render times by using 'flat' shader (faster render) instead of OCPOM shader as the viewing angle becomes extreme

# Parallax Mapping Resources
Parallax Mapping at LearnOpenGL
https://learnopengl.com/Advanced-Lighting/Parallax-Mapping

Relaxed Cone Stepping Relief Mapping at NVidia
https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-18-relaxed-cone-stepping-relief-mapping

Relief Texture Mapping at University of North Carolina at Chapel Hill
https://www.inf.ufrgs.br/~oliveira/pubs_files/RTM.pdf

Blender Cycles Node Optimizations
https://docs.blender.org/manual/en/latest/render/cycles/optimizations/nodes.html
