# POMster
Parallax Occlusion Map addon for Blender

# Intro
Quickly create Parallax Occlusion Map textures with adjustable sample counts, and sharpen cycles, to get the best POM for the least cost.

Includes automated creation of Blender shader nodes, with user selectable node as the base heightmap (custom group nodes are allowed/encouraged).

# Work In Progress (WIP)
Still a prototype, major changes underway...

Adjustable sample counts, and sharpen cycles are currently WIP. Only 3 and 1 implemented so far, but results are encouraging.

## Math Shortcuts (boring, but explains the nodes)
POMster implements Parallax Occlusion Map (POM) textures by taking advantage of some math shortcuts:
1) If the displacement height at the UV coordinates before applying POM match the height at the UV coordinates after applying POM, then the amount of error (visual warping) is zero.
  - i.e. the displacement height "in" should equal the displacement height "out"
  - this is used to easily get the estimated error value for any input displacement height by subtracting height in from height out
  - avoid messy UV calculations, just one value: height
2) A quick spread sample is calculated given a "center" and a "radius", height samples before and after can be compared/biased to get a "best" sample.
  - sample points are spaced equidistant from each other, high to low
  - e.g. sample 1 is "highest", sample 3 is "lowest"
3) The signs of the sample error values "point to" the most accurate sample(s).
  - similar to the way a magnetic compass needle points towards Earth's magnetic poles
    - e.g. if the highest sample(s) have negative error, and the lowest sample(s) have positive error, then the "compass needles" (error sign values) are pointing to the middle sample(s), so bias towards the middle sample(s)
  - bias towards high displacement samples and away from low displacement samples at the same time by only adding weight if the sign is positive ("compass needle" points towards up)
  - biasing does not eliminate samples, and multiple heights may be correct (e.g. at shallow angles to the mesh face), so further refinement is needed
5) Cutoff Quadrants, keep only the lowest average error, highest average displacement sample(s).
  A) calculate average absolute error, take only sample(s) below or equal to average absolute error
  B) calculate average of remaining sample height(s), take only remaining sample(s) above or equal to average height
  - this cuts the number of samples in half, or less
  - repeat the Cutoff Quadrants nodegroup as needed, to reduce number of samples to 1
    - e.g. if 8 original samples were taken then use Cutoff Quadrants 3 times successively to get only the best 1 out of 8 samples
  - the nodegroup will never reduce number of remaining samples to less than 1 (because average value of one sample equals itself)

# Congratulations, you read me to the end!
