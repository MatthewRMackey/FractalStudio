from .FractalWidget import FractalWidget

import torch
from torch import complex64

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class JuliaWidget(FractalWidget):
    def __init__(self, parent=None, width=600, height=800, c=complex(-.5,-.5)):
        super().__init__(parent, width, height)
        self.c = c
        self.julia = self.generate((-2,-2), (-2, 2), self.width, self.height, self.depth, self.power)

    def generate(self, r_range: tuple, i_range: tuple, r_sgmts: int, i_sgmts: int, depth: int, power: float):
        # Generate a 2D grid of complex numbers for initial z values
        x = torch.linspace(r_range[0], r_range[1], r_sgmts, dtype=torch.float32)
        y = torch.linspace(i_range[0], i_range[1], i_sgmts, dtype=torch.float32)
        x, y = torch.meshgrid(x, y, indexing="xy")

        # Move the grid to the GPU
        x, y = x.cuda(), y.cuda()
        z = x + 1j * y

        # Set the Julia set constant c to self.center
        c_real, c_imag = self.c.real, self.c.imag
        c = torch.complex(torch.full_like(x, c_real), torch.full_like(y, c_imag))

        escape_depth = torch.zeros_like(x, dtype=torch.float32, device='cuda')
        escaped = torch.zeros_like(x, dtype=torch.bool, device='cuda')

        for i in range(depth):
            z = z ** power + c
            escaped = torch.abs(z) > 2

            newly_escaped = escaped & (escape_depth == 0)
            escape_depth[newly_escaped] = i + 1

            if torch.all(escaped):
                break

        # Optional: Implement smooth coloring
        # log_zn = torch.log(torch.abs(z)) / 2**power
        # nu = torch.log(log_zn / torch.log(torch.tensor(2.0))) / torch.log(torch.tensor(2.0))
        # smooth_iter = i + 1 - nu
        # escape_depth = torch.where(escaped, smooth_iter, torch.tensor(depth, dtype=torch.float32))

        return escape_depth.cpu().tolist()