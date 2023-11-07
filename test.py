import qutip as qt
import numpy as np
tmax=700000
time_lis=np.linspace(0,tmax,30000)
n=3
init_state = qt.Qobj([[np.sqrt(1 / n)], [np.sqrt((n - 1) / n)]])
hmlta = qt.Qobj([[1 - 1 / n, -np.sqrt(n - 1) / n], [-np.sqrt(n - 1) / n, 1 - (n - 1) / n]])
hmltb = qt.Qobj([[0,0], [0,1]])
a=qt.mesolve([[hmlta,lambda x,*arg:(tmax-x)/tmax],[hmltb,lambda x,*arg : x/tmax]], init_state, time_lis, [], [])
print(np.abs(a.states)[-1])