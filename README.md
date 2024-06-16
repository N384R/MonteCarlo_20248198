## Term Paper for Statistical Mechanics

Edited by 20248198 Jeyun Ju

Inside the MonteCarlo directory, there is:

    system.py:
        to construct the system to simulate

    ising.py:
        to run the MC simulation

example:

    from MonteCarlo import System, Ising

    system = System(10, J=1)
    ising = Ising(system)

    ising.run_eq(T_start=10, T_end=0.1, dT=0.1, steps=5000)
