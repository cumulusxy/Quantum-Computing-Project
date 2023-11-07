import qutip as qt
import numpy as np


class QSystem:
    def __init__(self, init_state, hamiltonian, time_lis):
        self.init_state = init_state
        self.hamiltonian = hamiltonian
        self.time_lis = time_lis
        self.state_lis = close_evolve(init_state, hamiltonian, time_lis)

    def slice_coordinate(self):
        return tuple(self.state_lis[:, i] for i in range(np.shape(self.state_lis)[1]))

class AQCSystem(QSystem):
    def __init__(self, init_state, hamiltonian_lis, time_schedule, dimless_time_lis, tf):
        time_lis = dimless_time_lis * tf
        time_schedule_lis=[lambda x,*args: time_schedule(x,tf,*args)[i] for i in range(len(hamiltonian_lis))]
        hamiltonian = [[ham, sch] for ham, sch in zip(hamiltonian_lis, time_schedule_lis)]
        super().__init__(init_state, hamiltonian, time_lis)


def close_evolve(initState, hamiltonian, time_lis):
    objLis = qt.mesolve(hamiltonian, initState, time_lis, [], [])
    stateLis = [state for state in objLis.states]
    return np.array(stateLis)

def simple_time_schedule(x, tf, *args):
    return (tf-x)/tf, x/tf

def optimal_time_schedule(x, tf, n, *args):
    n=2
    s = x / tf
    a = 1 / 2 - 1 / (2 * np.sqrt(n - 1)) * np.tan((2 * s - 1) * np.arctan(np.sqrt(n - 1)))
    b = 1 / 2 + 1 / (2 * np.sqrt(n - 1)) * np.tan((2 * s - 1) * np.arctan(np.sqrt(n - 1)))
    return a, b

if __name__ == "__main__":
    state = qt.Qobj([[1], [0]])
    hamiltonian = qt.Qobj([[1, 0], [0, -1]])
    stateLis = close_evolve(state, hamiltonian, np.arange(0, 100, 1))
    print(stateLis[-1])
