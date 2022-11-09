# POMster
Parallax Occlusion Map addon for Blender

# Intro
Quickly create Parallax Occlusion Map textures with adjustable sample counts, and sharpen cycles, to get the best POM for the least cost.

Includes automated creation of Blender shader nodes, with user selectable node as the base heightmap (custom group nodes are allowed/encouraged).

# Work In Progress (WIP)
Still a prototype, major changes underway...

Adjustable sample counts, and sharpen cycles are currently WIP. Only 3 and 1 implemented so far, but results are encouraging.

## How It Works
POMster implements Parallax Occlusion Map (POM) textures by making use of some observations:
1) Zero Error where POM Height In equals POM Height Out
  - if the displacement height at the UV coordinates before applying POM is the same as the height at the UV coordinates after applying POM, then the amount of error (visual warping) is zero
    - i.e. the displacement height "in" should equal the displacement height "out"
  - this is used to easily get the estimated error value for any input displacement height by subtracting height in from height out
  - avoid messy UV calculations, just a one-dimensional value to sample: height
2) Higher Parts of POM Texture Appear Closer to Viewer
  - higher samples occlude lower samples
3) Evenly Spread Sample for First Approximation
  - quick spread sample is calculated given a "center" and a "radius"
  - ordered sample points are spaced equidistant from each other, high to low
    - e.g. sample 1 is "highest", sample 3 is "lowest"
  - height samples can be compared/weighted later to calculate error, and a "best" sample found
4) The Signs of the Sample Error Values "Point to" the Most Accurate Sample(s)
  - similar to the way a magnetic compass needle points towards Earth's magnetic poles
    - e.g. if highest sample(s) have negative error, and lowest sample(s) have positive error, then "compass needles" (error sign values) are pointing to middle sample(s), so bias towards middle sample(s)
  - may be more than one "correct" (zero error) sample - e.g. if view ray would pass through high point first and lower point(s) later
  - bias towards high displacement samples, and use error sign information to also bias towards "best" sample(s), by only adding weight if the error sign is positive ("compass needle" points towards up)
  - biasing does not eliminate samples, and multiple heights may be correct (e.g. at shallow angles to the mesh face)
  -further refinement is needed
5) Reduce Sample Count to Best Samples
  - apply two successive cutoffs, in multiple cycles, weighting worst samples to zero
  - keep only the lowest average error, highest average displacement sample(s)
    1) calculate average absolute error, take only sample(s) below or equal to average absolute error
    2) calculate average of remaining sample height(s), take only remaining sample(s) above or equal to average height
  - this cuts the number of samples in half, or less
  - repeat the Cutoff Quadrants nodegroup as needed, to reduce number of samples to 1
    - e.g. if 8 original samples were taken then use Cutoff Quadrants 3 times successively to get only the best 1 out of 8 samples
  - the nodegroup will never reduce number of remaining samples to less than 1 (because average value of one sample equals itself)

# Congratulations, you read me to the end!
