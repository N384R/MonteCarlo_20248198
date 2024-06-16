import numpy as np

class Ising:
    def __init__(self, target):
        self.target = target
        self.results = {
            'magnetization': {},
            'energy': {},
            'specific_heat': {},
            'susceptibility': {}
        }

    def step(self, T):
        n = self.target.lattice.shape[0]
        x, y = np.random.randint(0, n, size=2)
        dE = self.target.delta_energy(x, y)
        if dE <= 0 or np.random.rand() < np.exp(-dE / T):
            self.target.lattice[x, y] *= -1
        return self.target

    def run_eq(self, T_start=10, T_end=0.1, dT=0.1, steps=5000):
        j = self.target.J
        temperatures = np.arange(T_start, T_end-dT, -dT)
        initial_state = self.target.lattice.copy()
        for T in temperatures:
            self.target.lattice = initial_state.copy()
            energies = np.zeros(steps)
            magnetizations = np.zeros(steps)

            for step in range(steps):
                self.step(T * j)
                magnetizations[step] = self.target.magnetization()
                energies[step] = self.target.energy()

            if np.isclose(T, T_start) or np.isclose(T, T_end):
                print(f'T = {T:.02f}')
                print(self.target.lattice)

            mag = self.target.magnetization()
            en = self.target.energy()
            spe_heat = self.target.specific_heat(energies, T)
            susc = self.target.susceptibility(magnetizations, T)

            self.results['magnetization'][T] = mag
            self.results['energy'][T] = en
            self.results['specific_heat'][T] = spe_heat
            self.results['susceptibility'][T] = susc

            print(f'T = {T:5.02f}, M = {mag:6.03f}, E = {en:6.03f}, C = {spe_heat:.02e}, X = {susc:.02e}')

    def run_non_eq(self, T=8, H_lmax=0, H_rmax=10, dH=0.1, steps=5000):
        n = self.target.lattice.size
        j = self.target.J
        H_values = np.concatenate((np.arange(0, H_rmax, dH),
                                   np.arange(H_rmax, H_lmax, -dH),
                                   np.arange(H_lmax, H_rmax+dH, dH)))

        for _ in range(steps):
            self.step(T * j)

        for H in H_values:
            self.target.H = H
            for _ in range(self.target.gamma * n):
                self.step(T * self.target.J)

            mag = self.target.magnetization()
            en = self.target.energy()

            self.results['magnetization'][H] = mag
            self.results['energy'][H] = en

            print(f'H = {H:6.03f}, M = {mag:6.03f}, E = {en:6.03f}')

        self.target.H = 0
