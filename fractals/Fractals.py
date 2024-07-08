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
        # c = x + 1j * y
        # z = torch.zeros_like(c)
        z = x + 1j * y
        c = .35 + 0.06j  # Fixed complex number for the Julia set


        # Initialize arrays to store the results
        escape_depth = torch.zeros_like(x, dtype=torch.float32, device='cuda')
        escaped = torch.zeros_like(x, dtype=torch.bool, device='cuda')

        for i in range(depth):
            # Update the values of z
            z = z ** power + c

            # Check for escape condition
            new_escaped = torch.abs(z) > 2

            # Update escape_depth only for pixels that have just escaped
            just_escaped = new_escaped & ~escaped
            escape_depth[just_escaped] = i + 1 - torch.log(torch.log(torch.abs(z[just_escaped]))) / torch.log(torch.tensor(2.0))

            escaped = escaped | new_escaped

            # Break if all points have escaped
            if torch.all(escaped):
                break

        # Set escape_depth to depth for points that never escaped
        escape_depth[~escaped] = depth
        
        # Rotate and mirror operations
        # escape_depth = torch.flip(escape_depth, [0, 1])
        # escape_depth = torch.flip(escape_depth, [0])

        return escape_depth.cpu().tolist()