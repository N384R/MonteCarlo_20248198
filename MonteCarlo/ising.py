import numpy as np

class Ising:
    def __init__(self, target):
        self.target = target

    def _step(self, T):
        n = self.target.lattice.shape[0]
        x, y = np.random.randint(0, n, size=2)
        dE = self.target.delta_energy(x, y)
        if dE <= 0 or np.random.rand() < np.exp(-dE / T):
            self.target.lattice[x, y] *= -1
        return self.target

    def run(self, init, fin, delta, steps):
        j = self.target.J
        temperatures = np.arange(init, fin, -delta)
        initial_state = self.target.lattice.copy()
        for T in temperatures:
            self.target.lattice = initial_state.copy()
            energies = []
            magnetizations = []
            for _ in range(steps):
                self._step(T * j)
                energies.append(self.target.energy())
                magnetizations.append(self.target.magnetization())

            magnetization = self.target.magnetization()
            energy = self.target.energy()
            specific_heat = self.target.specific_heat(energies, T)
            susceptibility = self.target.susceptibility(magnetizations, T)
            yield (T, magnetization, energy, specific_heat, susceptibility)
