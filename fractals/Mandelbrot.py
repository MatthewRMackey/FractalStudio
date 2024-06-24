import torch
from torch import complex64

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Mandelbrot:
    def __init__(self, r_range=(-2,2), 
                 i_range=(-2,2), 
                 w_sgmts=800, 
                 h_sgmts=600, 
                 m_depth=10,
                 power=2) -> None:
        self.r_range = r_range
        self.i_range = i_range
        self.w_sgmts = w_sgmts
        self.h_sgmts = h_sgmts
        self.m_depth = m_depth
        self.power = power
        self.generateManEscapes()
    
    def generateManEscapes(self):
        # Generate a 2D grid of complex numbers
        x = torch.linspace(self.r_range[0], self.r_range[1], self.w_sgmts)
        y = torch.linspace(self.i_range[0], self.i_range[1], self.h_sgmts)
        x, y = torch.meshgrid(x, y, indexing="xy")

        # Move the grid to the GPU
        x, y = x.cuda(), y.cuda()
        z = x + 1j * y

        # Initialize arrays to store the results
        escape_depth = torch.zeros_like(x, dtype=torch.float32, device='cuda')

        for i in range(self.m_depth):

            # Check for escape condition
            escaped = torch.abs(z) <= 2
            
            # Update escape_depth only for pixels that have not escaped
            mask = torch.where(~escaped, torch.tensor(0, dtype=torch.float32), torch.tensor(1, dtype=torch.float32))
            escape_depth += mask

            # Update the values of z
            z = z ** self.power + x + 1j * y

        inset = escape_depth == self.m_depth
        mask = torch.where(inset, torch.tensor(self.m_depth, dtype=torch.float32), torch.tensor(0, dtype=torch.float32))
        escape_depth -= mask
        self.escapes = escape_depth.tolist()