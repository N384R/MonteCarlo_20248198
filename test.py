#%%
import matplotlib.pyplot as plt
from MonteCarlo import Ising, System

N = 10
system = System(N, J=1)
metropolis = Ising(system)

temperatures = []
magnetizations = []
energies = []
specific_heats = []
susceptibilities = []

for T, mag, en, heat, sus in metropolis.run(10, 0.1, 0.1, 1000):
    print(f'{T:.03f}, {mag:6.03f}')
    temperatures.append(T)
    magnetizations.append(mag)
    energies.append(en)
    specific_heats.append(heat)
    susceptibilities.append(sus)

fig, ax = plt.subplots(1, 4, figsize=(10, 5))
plt.subplots_adjust(wspace=0.7)
fig.set_facecolor('white')

ax[0].plot(temperatures, magnetizations, marker='o', linestyle='-', color='black')
ax[0].set_xlabel('Temperature (T)')
ax[0].set_ylabel('Magnetization')

ax[1].plot(temperatures, energies, marker='o', linestyle='-', color='blue')
ax[1].set_xlabel('Temperature (T)')
ax[1].set_ylabel('Energy')

ax[2].plot(temperatures, specific_heats, marker='o', linestyle='-', color='red')
ax[2].set_xlabel('Temperature (T)')
ax[2].set_ylabel('Specific Heat')

ax[3].plot(temperatures, susceptibilities, marker='o', linestyle='-', color='green')
ax[3].set_xlabel('Temperature (T)')
ax[3].set_ylabel('Susceptibility')
