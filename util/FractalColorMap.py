import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

class FractalColorMap:
    def __init__(self, map_name="default", num_colors = 50):
        self.map_name = map_name
        self.num_colors = num_colors
        self.file_name = "./color_maps/color_maps.json"
        self.map_dict = self.load_color_json()
        self.color_map = self.build_color_map()

    def load_color_json(self):
        with open(self.file_name, 'r') as file:
            return json.load(file)

    def write_color_json(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.map_dict, file, indent=2)

    def add_color_scheme(self, name, colors):
        self.map_dict[name] = colors

    def apply_colormap(self, escape_depths):
        colored_fractal = []

        # Apply the colormap
        for row in escape_depths:
            colored_fractal.append(list(map(lambda e: self.color_map[int(e)%self.num_colors], row)))

        return np.array(colored_fractal)
    
    def build_color_map(self):
        basis_colors = self.map_dict[self.map_name]
        color_map = []
        k = len(basis_colors) - 1

        for i in range(self.num_colors):
            t = i / (self.num_colors - 1)
            j = int(t * k)

            if j == k:
                color = basis_colors[j]
            else:
                t_interp = (t - j / k) * k
                color = self.lerp_color(basis_colors[j], basis_colors[j + 1], t_interp)

            color_map.append(color)

        return color_map

    def lerp_color(self, color1, color2, t):
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))