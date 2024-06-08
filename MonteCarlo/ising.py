import numpy as np

class Ising:
    def __init__(self, target):
        self.target = target

    def step(self, T):
        n = self.target.lattice.shape[0]
        x, y = np.random.randint(0, n, size=2)
        dE = self.target.delta_energy(x, y)
        if dE <= 0 or np.random.rand() < np.exp(-dE / T):
            self.target.lattice[x, y] *= -1
        return self.target

    def run_eq(self, T_start=10, T_end=0.1, dT=0.1, steps=1000):
        j = self.target.J
        temperatures = np.arange(T_start, T_end, -dT)
        initial_state = self.target.lattice.copy()
        for T in temperatures:
            self.target.lattice = initial_state.copy()
            energies = np.zeros(steps)
            magnetizations = np.zeros(steps)
            for step in range(steps):
                self.step(T * j)
                magnetizations[step] = self.target.magnetization()
                energies[step] = self.target.energy()

            magnetization = self.target.magnetization()
            energy = self.target.energy()
            specific_heat = self.target.specific_heat(energies, T)
            susceptibility = self.target.susceptibility(magnetizations, T)
            yield (T, magnetization, energy, specific_heat, susceptibility)

    def run_non_eq(self, T=8, H_start=0, H_end=10, dH=0.1):
        n = self.target.lattice.size
        H_values = np.concatenate((np.arange(H_start, H_end, dH),
                                   np.arange(H_end, H_start-dH, -dH)))
        initial_state = self.target.lattice.copy()
        for H in H_values:
            self.target.lattice = initial_state.copy()
            self.target.H = H
            for _ in range(self.target.gamma * n):
                self.step(T * self.target.J)

            magnetization = self.target.magnetization() / n
            energy = self.target.energy() / n
            yield (H, magnetization, energy)

        self.target.H = 0
