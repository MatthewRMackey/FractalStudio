from .FractalWidget import FractalWidget

import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SierpinskiWidget(FractalWidget):
    def __init__(self, parent=None, width=600, height=800, sides=3):
        super().__init__(parent, width, height)
        self.sides = sides if sides > 2 else 3
        self.sierpinski = self.generate()

    def generate(self):
        return