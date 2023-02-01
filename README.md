# POMster: Parallax Occlusion Mapping addon for Blender

[Download Latest Release](https://github.com/DreamSpoon/POMster/releases/latest)

* Create materials with depth/hologram effect
* Replace millions of faces of geometry with a single face, by using Displacement texture with POMster nodes
* Two types of POM:
  1. Material Shader nodes - only a shader is needed, with UV Map, to add depth effect
  2. Geometry Nodes modifier - "shells" and "fringe" geometry are created to add depth effect, with better shadowing, and fringe at edges where near geometry masks far geometry - "bumpy" edges
* Builtin tools to help blend between POM geometry (low poly count) and actual subdivided geometry (high poly count)
* Works with EEVEE and Cycles
* Works with pre-generated and procedurally-generated textures, but is more efficient with pre-generated textures

# Installation
Download [latest release](https://github.com/DreamSpoon/POMster/releases/latest)

Start Blender, then look in menu near top of Blender window.

`Edit -> User Preferences -> Add-ons -> Install from File...`

Choose the downloaded POMster release zip file and press the Install Addon button.

Enable the addon while still in User Preferences menu.

Once installed and enabled, the add-on can be found in these places:
  1) *3DView* window, the tools menu on right side of 3D view window
  2) *Shader Nodes Editor* window, the tools menu on right side of node editor window
  3) *Geometry Nodes Editor* window, the tools menu on right side of node editor window

Each of these places has a *POMster* tab for access to POMster functions.

# Usage Video

[Parallax Occlusion Mapping with POMster for Blender - Part 1](https://youtu.be/BspcE3a6aVQ)

# Usage Docs

## [Material Shader Nodes](docs/MAT_SHADER_NODES.md)

## [Geometry Nodes](docs/GEOMETRY_NODES.md)

# See Also
Parallax Mapping at LearnOpenGL
https://learnopengl.com/Advanced-Lighting/Parallax-Mapping

Relaxed Cone Stepping Relief Mapping at NVidia
https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-18-relaxed-cone-stepping-relief-mapping

Relief Texture Mapping at University of North Carolina at Chapel Hill
https://www.inf.ufrgs.br/~oliveira/pubs_files/RTM.pdf

Blender Cycles Node Optimizations
https://docs.blender.org/manual/en/latest/render/cycles/optimizations/nodes.html
