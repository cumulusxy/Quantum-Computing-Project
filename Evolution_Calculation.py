import qutip as qt
import numpy as np


class QSystem:
    def __init__(self, init_state, hamiltonian, time_lis):
        self.init_state = init_state
        self.hamiltonian = hamiltonian
        self.time_lis = time_lis
        self.state_lis = close_evolve(init_state, hamiltonian, time_lis)
        self.ground_state = get_ground_state(hamiltonian, time_lis)

    def slice_coordinate(self):
        return tuple(self.state_lis[:, i] for i in range(np.shape(self.state_lis)[1]))

class AQCSystem(QSystem):
    def __init__(self, init_state, hamiltonian_lis, time_schedule, dimless_time_lis, tf):
        time_lis = dimless_time_lis * tf
        time_schedule_lis=[lambda x,*args,i=i: time_schedule(x,tf,i,*args) for i in range(len(hamiltonian_lis))]
        hamiltonian = [[ham, sch] for ham, sch in zip(hamiltonian_lis, time_schedule_lis)]
        super().__init__(init_state, hamiltonian, time_lis)


def close_evolve(initState, hamiltonian, time_lis):
    objLis = qt.mesolve(hamiltonian, initState, time_lis, [], [])
    stateLis = [state for state in objLis.states]
    return np.array(stateLis)

def simple_time_schedule(x, tf, coeff_pos, *args):
    if coeff_pos == 0:
        return (tf-x)/tf
    elif coeff_pos == 1:
         return x/tf

def optimal_time_schedule(x, tf, coeff_pos,n, *args):
    s = x / tf
    if coeff_pos ==0:
        return 1 / 2 - 1 / (2 * np.sqrt(n - 1)) * np.tan((2 * s - 1) * np.arctan(np.sqrt(n - 1)))
    elif coeff_pos ==1:
        return 1 / 2 + 1 / (2 * np.sqrt(n - 1)) * np.tan((2 * s - 1) * np.arctan(np.sqrt(n - 1)))

def generate_dimless_timelis(tf_lis,sample_number1):
    return tuple(np.linspace(0,1, int(sample_number1*tf_lis[i]/tf_lis[0])) for i in range(len((tf_lis))))


def match_by_padding(*args):
    args = [lst for lst in args]
    len_lis=[len(lst) for lst in args]
    len_max=np.max(len_lis)
    return tuple(np.pad(args[i],(0,len_max-len_lis[i]),"edge") for i in range(len(args)))

def get_ground_state(hamiltonian,time_lis):
    ham_t=np.array([np.zeros(np.shape(hamiltonian[0][0])) for _ in range(len(time_lis))])
    for t in range(len(ham_t)):
        for ham_pair in hamiltonian:
            ham_t[t]+=ham_pair[0].data*ham_pair[1](time_lis[t])
    ground_state_lis=np.array([qt.Qobj(ham).groundstate()[1] for ham in ham_t])
    return ground_state_lis

if __name__ == "__main__":
    state = qt.Qobj([[1], [0]])
    hamiltonian = qt.Qobj([[1, 0], [0, -1]])
    stateLis = close_evolve(state, hamiltonian, np.arange(0, 100, 1))
    print(stateLis[-1])
