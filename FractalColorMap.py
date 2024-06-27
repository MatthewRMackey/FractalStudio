import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from Fractals import Fractals

class FractalColorMap:
    def __init__(self, name="default"):
        self.name = name
        self.file_name = "./color_maps/color_maps.json"
        self.color_dict = self.load_color_json()
        self.color_map = self.build_color_map()

    def load_color_json(self):
        with open(self.file_name, 'r') as file:
            return json.load(file)

    def write_color_json(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.color_dict, file, indent=2)

    def add_color_scheme(self, name, colors):
        self.color_dict[name] = colors

    def build_color_map(self, num_colors=10):
        colors = self.color_dict[self.name]
        if not colors:
            raise ValueError(f"No colors found for scheme '{self.name}'")

        # Normalize the color values to be between 0 and 1
        normalized_colors = [[r/255, g/255, b/255] for r, g, b in colors]

        # Create evenly spaced positions for each color
        positions = np.linspace(0, 1, len(normalized_colors))

        # Create the color map
        return LinearSegmentedColormap.from_list(self.name, list(zip(positions, normalized_colors)), N=10)

    def apply_colormap(self, escape_depths, max_depth):
        # Normalize the escape depths
        normalized_depths = np.array(escape_depths) / max_depth

        # Ensure the values are in the range [0, 1]
        normalized_depths = np.clip(normalized_depths, 0, 1)

        # Apply the colormap
        colored_fractal = self.color_map(normalized_depths)

        # Convert to RGB integer values
        rgb_fractal = (colored_fractal[:, :, :3] * 255).astype(np.uint8)

        return rgb_fractal 