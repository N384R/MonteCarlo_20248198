import numpy as np

class System:
    def __init__(self, n, **kwargs):
        self.lattice = np.ones((n, n), dtype=int)
        self.J = kwargs.get('J', 1)

    def neighbors(self, x, y):
        n = self.lattice.shape[0]
        left  = self.lattice[x, (y-1)%n]
        right = self.lattice[x, (y+1)%n]
        up    = self.lattice[(x-1)%n, y]
        down  = self.lattice[(x+1)%n, y]
        return left, right, up, down

    def delta_energy(self, x, y):
        return 2 * self.J * self.lattice[x, y] * sum(self.neighbors(x, y))

    def energy(self):
        n = self.lattice.shape[0]
        energy = 0
        for i in range(n):
            for j in range(n):
                spin = self.lattice[i, j]
                energy -= self.J * spin * sum(self.neighbors(i, j))
        return energy/2

    def magnetization(self):
        return np.sum(self.lattice) / self.lattice.size

    def specific_heat(self, energies, T):
        beta = 1 / T
        avg_energy = np.mean(energies)
        avg_energy_sq = np.mean([e**2 for e in energies])
        return (avg_energy_sq - avg_energy**2) * beta**2 / self.lattice.size

    def susceptibility(self, magnetizations, T):
        beta = 1 / T
        avg_mag = np.mean(magnetizations)
        avg_mag_sq = np.mean([m**2 for m in magnetizations])
        return (avg_mag_sq - avg_mag**2) * beta / self.lattice.size
