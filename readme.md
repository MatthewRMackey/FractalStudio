# Fractal Studio

## Features (and Future Features)
1. GUI using PyQT5
2. Fractal displays (Mandelbrot/Julia currently) calculated using PyTorch tensors to leverage CUDA cores for improved speed.
3. Adjust the type of fractal, zoom depth, zoom factor, center, fractal power, and color map on-the-fly.
4. Click-to-center and scroll-to-zoom interactivity.
5. Integer and Fractional Escape Depth Calculations
6. Custom Color Maps for both integer and fractional sets.
7. Zoom-to functionality: zooms from default to current center and zoom factor.
8. Save Image with center, zoom, type, and map metadata.
9. Save zoom videos and various coloring animations.

## TODO
- [ ] Algebraic Optimizations (reducing number of multiplications -> O(n<sup>2</sup>) for multiplication)
- [ ] Fix Reset All Button
- [ ] Add an entry box for c in the julia set and fix backend so when julia is generated c=center
- [ ] Fix save image location, and figure out method for metadata collection for each image
- [ ] Add linear panning functionality across all changeable variables (power, depth, center, julia c, and zoom factors)
- [ ] Add julia morphing following cursor path
- [ ] Add smooth/fractional escape capabilities
- [ ] Add settings file that default values and things like discrete/smooth coloring, resolution, etc can be loaded from on startup.
- [ ] Improve visual look of the configuration/options panel (rename to options... config will become a preset file).
- [ ] Fix error when clicking in the whitespace of options panel.

## Important References
- [Algebraic Optimizations.](https://randomascii.wordpress.com/2011/08/13/faster-fractals-through-algebra/)
- [Spektre on fractional escapes, infinitely small numbers, and perturbation theory.](https://stackoverflow.com/questions/66709289/what-are-the-fastest-algorithms-for-rendering-the-mandelbrot-set)
- [Multiplication Algorithms Wikipedia.](https://en.wikipedia.org/wiki/Multiplication_algorithm#Lattice_multiplication)
- [Plotting Algorithm for Mandelbrot Wikipedia.](https://en.wikipedia.org/wiki/Plotting_algorithms_for_the_Mandelbrot_set)
- [Creating Images from Voronoi Diagrams(2020) - might create a texture effect.](https://github.com/nickvdw/image-to-voronoi)

## Discrete Coloring Examples
### Mandelbrot

![](./imgs/mandelbrot/output_image_0.png "Mandelbrot: z=.5, center=(0,0), depth=100, 50 colors")
![](./imgs/mandelbrot/output_image_1.png "Mandelbrot: z=384.5, center=(0.35140000000000005,-0.0636734693877551), depth=250, 50 colors")
![](./imgs/mandelbrot/output_image_2.png "Mandelbrot: z=2493.942547559738, center=(-0.7898941570950317,-0.15798088570332877), depth=150, 50 colors")
![](./imgs/mandelbrot/output_image_3.png "Mandelbrot: z=3243.658447265625, center=(-0.00990808131251567,-0.6575198381127177), depth=225, 50 colors")
![](./imgs/mandelbrot/output_image_4.png "Mandelbrot: z=4, power=1.09, center=(0,0), depth=100, 50 colors")

### Julia

![](./imgs/julia/output_image_0.png "Julia: z=.75, center=(0,0), c=(-0.00990808131251567,-0.6575198381127177), depth=225, 50 colors")
![](./imgs/julia/output_image_1.png "Julia: z=.75, center=(0,0), c=(-0.528,-0.5102040816326531), depth=100, 50 colors")
![](./imgs/julia/output_image_2.png "Julia: z=.5, center=(0,0), c=(-1.012,-0.32244897959183677), depth=100, 50 colors")
![](./imgs/julia/output_image_3.png "Julia: z=.5, power=1.09, center=(0,0), c=(-0.044,0.0163265306122449), depth=100, 50 colors")
