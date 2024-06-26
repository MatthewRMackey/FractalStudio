import torch
from torch import complex64

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Fractals:
    
    def generateMandelbrot(self, r_range: tuple, i_range: tuple, r_sgmts: int, i_sgmts: int, depth: int, power: float):
        # Generate a 2D grid of complex numbers
        x = torch.linspace(r_range[0], r_range[1], r_sgmts)
        y = torch.linspace(i_range[0], i_range[1], i_sgmts)
        x, y = torch.meshgrid(x, y, indexing="xy")

        # Move the grid to the GPU
        x, y = x.cuda(), y.cuda()
        z = x + 1j * y

        # Initialize arrays to store the results
        escape_depth = torch.zeros_like(x, dtype=torch.float32, device='cuda')

        for i in range(depth):

            # Check for escape condition
            escaped = torch.abs(z) <= 2
            
            # Update escape_depth only for pixels that have not escaped
            mask = torch.where(~escaped, torch.tensor(0, dtype=torch.float32), torch.tensor(1, dtype=torch.float32))
            escape_depth += mask

            # Update the values of z
            z = z ** power + x + 1j * y

        inset = escape_depth == depth
        mask = torch.where(inset, torch.tensor(depth, dtype=torch.float32), torch.tensor(0, dtype=torch.float32))
        escape_depth -= mask
        return escape_depth.tolist()